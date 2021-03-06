# coding=utf-8
import collections
from datetime import datetime

from flask import session
from sqlalchemy import or_

import bmp.utils.timeutil as time
from bmp.utils.user_ldap import Ldap
from bmp import db
from bmp.const import PURCHASE
from bmp.const import USER_SESSION
from bmp.database import Database
from bmp.utils.exception import ExceptionEx

purchase_supplier = db.Table("purchase_supplier",
                             db.Column("purchase_id", db.Integer, db.ForeignKey("purchase.id")),
                             db.Column("supplier_id", db.Integer, db.ForeignKey("supplier.id")))

purchase_goods_category = db.Table("purchase_goods_category",
                                   db.Column("purchase_goods_id", db.Integer, db.ForeignKey("purchase_goods.id")),
                                   db.Column("category_id", db.Integer, db.ForeignKey("category.id")))

purchase_goods_spec = db.Table("purchase_goods_spec",
                               db.Column("purchase_goods_id", db.Integer, db.ForeignKey("purchase_goods.id")),
                               db.Column("category_id", db.Integer, db.ForeignKey("category.id")))


class PurchaseGoods(db.Model):  # 采购物品
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float)
    spec = db.relationship("Category",
                           secondary=purchase_goods_spec,
                           backref=db.backref("specs"),
                           uselist=False)

    amount = db.Column(db.Integer)
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))
    category = db.relationship("Category",
                               secondary=purchase_goods_category,
                               backref=db.backref("goods"),
                               uselist=False)

    def __init__(self, _dict):
        from bmp.models.asset import Category
        self.category = Category.query.filter(Category.id == _dict["category_id"]).one()
        self.price = _dict["price"]
        self.spec = Category.query.filter(Category.id == _dict["spec_id"]).one()
        self.amount = _dict["amount"]

    @staticmethod
    def _to_dict(self, inc_purchase=False):
        _dict = self.to_dict()
        category = self.category
        spec = self.spec
        purchase = self.purchase

        if category:
            _dict["category"] = category.to_dict()

        if spec:
            _dict["spec"] = spec.to_dict()

        for k, v in purchase.to_dict().items():
            if not _dict.__contains__(k):
                _dict[k] = v
        return _dict

    @staticmethod
    def between(beg, end):
        return [
            PurchaseGoods._to_dict(p, True)
            for p in PurchaseGoods.query
                .join(Purchase)
                .join(PurchaseApproval, PurchaseApproval.purchase_id == PurchaseGoods.purchase_id)
                .filter(PurchaseApproval.status != PURCHASE.FAIL)
                .filter(Purchase.is_finished == True)
                .filter(Purchase.is_draft == False)
                .filter(Purchase.apply_time >= beg)
                .filter(Purchase.apply_time <= end).all()
            ]


class PurchaseImg(db.Model):  # 比价图片
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    b64 = db.Column(db.Text)
    desc = db.Column(db.String(128))
    path = db.Column(db.String(256))
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))

    def __init__(self, _dict):
        if _dict.__contains__("b64"):
            self.b64 = _dict["b64"]
        else:
            self.b64 = ""
        self.desc = _dict["desc"]
        self.path = _dict["path"]

    @staticmethod
    def _to_dict(self):
        return self.to_dict()


class PurchaseApproval(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128))
    uid = db.Column(db.String(128), db.ForeignKey("user.uid"), nullable=False)
    status = db.Column(db.String(128), nullable=False)
    reson = db.Column(db.String(128))
    options = db.Column(db.String(128))
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.id"))
    approval_time = db.Column(db.DateTime)

    def __init__(self, _dict):
        self.type = _dict["type"]
        self.status = _dict["status"]
        self.reson = _dict["reson"]
        self.options = _dict["options"]
        self.uid = _dict["uid"]
        self.approval_time = datetime.now()

    @staticmethod
    def __next_approval_type(type):
        cur = PURCHASE.FLOW.index(type)
        if cur == len(PURCHASE.FLOW) - 1:
            return PURCHASE.FLOW[cur]
        return PURCHASE.FLOW[cur + 1]

    @staticmethod
    def edit(id, submit):
        approval = PurchaseApproval.query \
            .filter(PurchaseApproval.purchase_id == id) \
            .filter(PurchaseApproval.type == submit["type"])
        if approval.count():
            raise ExceptionEx("该节点已审批")

        _approval = PurchaseApproval(submit)
        purchase = Purchase.query.filter(Purchase.id == id).one()
        purchase.approvals.append(_approval)

        purchase.cur_approval_type = PurchaseApproval.__next_approval_type(_approval.type)

        if _approval.status == PURCHASE.FAIL:
            purchase.is_finished = True
        else:
            if _approval.type == PURCHASE.FLOW_TWO:
                total = sum([g.price * g.amount for g in purchase.goods])
                if total < PURCHASE.PRICE_LIMIT:
                    if not purchase.contract:
                        purchase.is_finished = True
                    else:
                        purchase.cur_approval_type = PURCHASE.FLOW_FOUR
            elif _approval.type == PURCHASE.FLOW_THREE:
                if not purchase.contract:
                    purchase.is_finished = True
            elif _approval.type == PURCHASE.FLOW_FOUR:
                purchase.is_finished = True

        db.session.commit()
        return purchase

    @staticmethod
    def _to_dict(self):
        return self.to_dict()


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    approvals = db.relationship("PurchaseApproval")
    contract = db.relationship("Contract", uselist=False, backref=db.backref("purchase"))
    imgs = db.relationship("PurchaseImg")
    goods = db.relationship("PurchaseGoods", backref=db.backref("purchase"))
    supplier = db.relationship("Supplier",
                               secondary=purchase_supplier,
                               backref=db.backref("purchases"),
                               uselist=False)

    cur_approval_type = db.Column(db.String(128))
    is_finished = db.Column(db.Boolean, default=False)
    is_draft = db.Column(db.Boolean, default=True)
    use = db.Column(db.Text)
    reson = db.Column(db.String(256))
    apply_uid = db.Column(db.String(128), db.ForeignKey("user.uid"), nullable=False)
    apply_businessCategory = db.Column(db.String(128), nullable=False)
    apply_time = db.Column(db.DateTime, nullable=False)

    def __eq__(self, other):
        return self.id == other.id

    def __init__(self, submit):
        goods, supplier, imgs, contract = submit["goods"], submit["supplier"], submit["imgs"], submit["contract"]
        if not submit.__contains__("id"):
            self.cur_approval_type = PURCHASE.FLOW_ONE
            self.apply_time = datetime.now()
            self.apply_businessCategory = session[USER_SESSION]["businessCategory"]
            self.apply_uid = session[USER_SESSION]["uid"]

        self.goods = [Database.to_cls(PurchaseGoods, g) for g in goods]
        self.supplier = supplier
        if isinstance(imgs, list): self.imgs = [Database.to_cls(PurchaseImg, img) for img in imgs]
        if contract: self.contract = contract
        self.use = submit["use"]
        if submit.__contains__("reson"):
            self.reson = submit["reson"]
        else:
            self.reson = ""

    @staticmethod
    def add(submit):
        purchase = Purchase(submit)
        db.session.add(purchase)
        db.session.commit()
        return purchase

    @staticmethod
    def get(id):
        from bmp.models.user import Group
        purchase = Purchase.query.filter(Purchase.id == id).one()
        purchase.cur_approval_type_desc = Group.get(purchase.cur_approval_type).desc
        return Purchase._to_dict(purchase, ["cur_approval_type_desc"])

    @staticmethod
    def _to_dict(self, cols=[]):
        _dict = self.to_dict(cols)
        _dict["approvals"] = [a.to_dict() for a in self.approvals]
        if self.contract:
            _dict["contract"] = self.contract.to_dict()
        _dict["imgs"] = [img.to_dict() for img in self.imgs]
        _dict["goods"] = [PurchaseGoods._to_dict(g) for g in self.goods]
        if self.supplier:
            _dict["supplier"] = self.supplier.to_dict()
        return _dict

    @staticmethod
    def __is_superior(uid, apply_uid):
        ldap = Ldap()
        if uid == ldap.get_2nd_manager(apply_uid):
            return True
        return False

    @staticmethod
    def finished(page=1, pre_page=20):
        from bmp.models.user import User

        uid = session[USER_SESSION]["uid"]
        group = set(User.get(uid)["group"]).intersection(PURCHASE.FLOW)

        page = Purchase.query \
            .join(PurchaseApproval) \
            .filter(or_(Purchase.apply_uid == uid,
                        PurchaseApproval.uid == uid,
                        PurchaseApproval.type.in_(group))) \
            .filter(Purchase.is_draft == False) \
            .filter(Purchase.is_finished == True) \
            .order_by(Purchase.apply_time.desc()).paginate(page, pre_page)

        return page.to_page(Purchase._to_dict)

    @staticmethod
    def unfinished(user_groups):
        from bmp.models.user import Group, User

        purchases = []
        uid = session[USER_SESSION]["uid"]
        group = set(User.get(uid)["group"]).intersection(PURCHASE.FLOW)
        group_map = {}
        for g in Group.select(to_dict=False):
            group_map[g.name.upper()] = g.desc

        for purchase in Purchase.query \
                .filter(Purchase.is_draft == False) \
                .filter(Purchase.is_finished == False).order_by(Purchase.apply_time.desc()).all():

            approvals = purchase.approvals
            apply_uid = purchase.apply_uid
            cur_approval_type = purchase.cur_approval_type
            purchase.cur_approval_type_desc = ""
            purchase.approval_enable = False
            is_append = False

            if group_map.__contains__(cur_approval_type.upper()):
                purchase.cur_approval_type_desc = group_map[cur_approval_type.upper()]

            if uid in [purchase.apply_uid] + [a.uid for a in approvals] \
                    or group.intersection([a.type for a in approvals]):
                purchases.append(purchase)
                is_append = True

            if cur_approval_type == PURCHASE.FLOW_ONE:
                if Purchase.__is_superior(uid, apply_uid):
                    purchase.approval_enable = True
                    if not is_append:
                        purchases.append(purchase)
            elif uid in user_groups[cur_approval_type]:
                purchase.approval_enable = True
                if not is_append:
                    purchases.append(purchase)
            else:
                continue
        return [Purchase._to_dict(p, ["approval_enable", "cur_approval_type_desc"]) for p in purchases]

    @staticmethod
    def passed(page=1, pre_page=20):
        return Purchase.query \
            .join(PurchaseApproval, PurchaseApproval.purchase_id == Purchase.id) \
            .filter(Purchase.is_finished == True) \
            .filter(PurchaseApproval.status != PURCHASE.FAIL) \
            .order_by(Purchase.apply_time.desc()) \
            .paginate(page, pre_page, False).to_page(Purchase._to_dict)

    @staticmethod
    def drafts(page=1, pre_page=20):
        page = Purchase.query \
            .filter(Purchase.apply_uid == session[USER_SESSION]["uid"]) \
            .filter(Purchase.is_draft == True) \
            .order_by(Purchase.apply_time.desc()) \
            .paginate(page, pre_page, False)
        return page.to_page(Purchase._to_dict)

    @staticmethod
    def delete(pid):
        db.session.delete(Purchase.query.filter(Purchase.id == pid).one())
        db.session.commit()

    @staticmethod
    def edit(submit):
        purchase = Database.to_cls(Purchase, submit)
        db.session.commit()

    @staticmethod
    def approval(pid):
        purchase = Purchase.query.filter(Purchase.id == pid).one()
        purchase.is_draft = False
        db.session.commit()
        return True

    @staticmethod
    def search(submit, page=None, pre_page=None):
        from bmp.models.asset import Category

        def check(s):
            if submit.__contains__(s):
                return submit[s]
            return False

        query = Purchase.query \
            .join(PurchaseGoods, PurchaseGoods.purchase_id == Purchase.id) \
            .join(purchase_goods_category) \
            .join(PurchaseApproval) \
            .join(Category) \
            .filter(Purchase.is_finished == True) \
            .filter(PurchaseApproval.status != PURCHASE.FAIL)

        if check("apply_businessCategory"):
            query = query.filter(Purchase.apply_businessCategory == submit["apply_businessCategory"])
        if check("apply_uid"):
            query = query.filter(Purchase.apply_uid == submit["apply_uid"])
        if check("apply_time_begin") and check("apply_time_end"):
            beg = datetime.strptime(submit["apply_time_begin"], "%Y-%m-%d")
            end = datetime.strptime(submit["apply_time_end"], "%Y-%m-%d")
            query = query.filter(Purchase.apply_time.between(beg, end))

        if check("goods"):
            parent = Category.query.filter(Category.name == submit["goods"]).one()
            childs = [c.id for c in Category.query.filter(Category.parent_id == parent.id).all()]
            query = query.filter(Category.id.in_(childs))
        if check("price_begin") and check("price_end"):
            goods = PurchaseGoods.query.filter(PurchaseGoods.purchase_id != None).all()
            pgoods = []
            for g in goods:
                total = g.price * g.amount
                if total >= int(submit["price_begin"]) and total <= int(submit["price_end"]):
                    pgoods.append(g.id)
            query = query.filter(PurchaseGoods.id.in_(pgoods))

        if page == None:
            return [Purchase._to_dict(p) for p in query.all()]

        return query.order_by(Purchase.apply_time.desc()).paginate(page, pre_page, False).to_page(Purchase._to_dict)

    @staticmethod
    def export(submit):
        # 申请人	申请部门	申请时间	物品	规格	数量	总价	审批人
        _export = []
        for purchase in Purchase.search(submit):
            for g in purchase["goods"]:
                _dict = collections.OrderedDict()
                _dict["采购编号"] = str(purchase["id"])
                _dict["总价"] = g["amount"] * g["price"]
                _dict["数量"] = g["amount"]
                _dict["规格"] = str(g["spec"]["name"])
                _dict["物品"] = str(g["category"]["name"])
                _dict["申请时间"] = time.format(purchase["apply_time"], "%Y-%m-%d")
                _dict["申请部门"] = str(purchase["apply_businessCategory"])
                _dict["申请人"] = str(purchase["apply_uid"])
                _export.append(_dict)
        return _export

    @staticmethod
    def between(beg, end):
        return [
            Purchase._to_dict(p)
            for p in Purchase.query
                .filter(Purchase.is_finished == True) \
                .filter(Purchase.is_draft == False) \
                .filter(Purchase.apply_time >= beg) \
                .filter(Purchase.apply_time <= end).all()
            ]


if __name__ == "__main__":
    pass

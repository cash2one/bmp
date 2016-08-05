# coding=utf-8
import json
from datetime import datetime

from bmp import db
from bmp.apis.base import BaseApi
from bmp.const import USER_SESSION, ACCESS
from bmp.models.access import Access
from bmp.tasks.mail.access import Mail
from bmp.utils.exception import ExceptionEx
from flask import session


class AccessApi(BaseApi):
    route = ["/access", "/access/<int:aid>", "/access/<int:page>/<int:pre_page>"]

    # 申请人 申请时间 类型 理由 内容 操作
    def get(self, page=0, pre_page=None, aid=0):
        if aid:
            return self.succ(Access.get(aid))

        return self.succ(Access.select(
            page=page,
            pre_page=pre_page,
            _filters=Access.status == ACCESS.NEW
        ))

    def post(self):
        submit = self.request()
        submit["apply_time"] = datetime.now()
        submit["apply_uid"] = session[USER_SESSION]["uid"]
        submit["content"] = json.dumps(submit["content"])

        Access.add(submit)
        return self.succ()

    def put(self, aid):
        submit = self.request()
        submit["id"] = aid
        if submit.__contains__("content"):
            submit["content"] = json.dumps(submit["content"])

        access = Access.edit(submit, auto_commit=False)

        if submit["status"] == ACCESS.APPROVAL:
            mail = Mail()
            if not mail.to(access):
                raise ExceptionEx("邮件发送失败")

        db.session.commit()
        return self.succ()

    def delete(self, aid):

        Access.delete(aid)
        return self.succ()


if __name__ == "__main__":
    pass

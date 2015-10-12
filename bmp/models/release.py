#coding: utf-8
from bmp import db
from datetime import datetime

'''
项目名称
发布时间
服务
类型
数据库
表名
从
抄送人
内容

申请人
申请时间
'''

class ReleaseService(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(128))
    type=db.Column(db.String(128))
    database=db.Column(db.String(128))
    table=db.Column(db.String(128))
    release_id=db.Column(db.Integer,db.ForeignKey("release.id"))
    def __init__(self,_dict):
        self.name=_dict["name"]
        self.type=_dict["type"]
        self.database=_dict["database"]
        self.table=_dict["table"]


class ReleaseApproval(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    type=db.Column(db.String(128))
    uid=db.Column(db.String(128))
    status=db.Column(db.String(128))
    reson=db.Column(db.String(128))
    other=db.Column(db.String(128))
    release_id=db.Column(db.Integer,db.ForeignKey("release.id"))

    def __init__(self,type):
        self.type=type
        self.status=u"待确认"


class Release(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    project=db.Column(db.String(128))
    _from=db.Column(db.String(128))
    to=db.Column(db.String(128))
    content=db.Column(db.String(256))
    copy_to_uid=db.Column(db.String(128))
    release_time=db.Column(db.DateTime)
    apply_uid=db.Column(db.String(128))
    apply_time=db.Column(db.DateTime)
    approvals=db.relationship("ReleaseApproval")
    service=db.relationship("ReleaseService",uselist=False)

    def __init__(self,_dict):
        self.project=_dict["project"]
        self._from=_dict["_from"]
        self.to=_dict["to"]
        self.release_time=datetime.strptime(_dict["release_time"],"%Y-%m-%d %H:%M:%S")
        self.copy_to_uid=_dict["copy_to_uid"]
        self.content=_dict["content"]


if __name__=="__main__":
    db.create_all()

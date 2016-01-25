# coding: utf-8
import re

from flask import render_template
from flask import request

import bmp.utils.mail as mail
from bmp.const import DEFAULT_GROUP, LEAVE
from bmp.models.user import User, Group
from bmp.models.ref import Ref
from bmp import log
from base import BaseMail


class Mail(BaseMail):
    def to(self, l):
        uids = [u.uid for u in Group.get_users(DEFAULT_GROUP.HR)] + [l.approval_uid]
        to = [User.get(uid)["mail"] for uid in uids]
        to.append("hr.dept@chinascopefinancial.com")

        sub = u"请假申请 编号:%d 申请人:%s" % (l.id, l.uid)

        self.send(
            to,
            sub,
            "/templates/leave/approval.html",
            "mail.leave.tpl.html",
            leave=l,
            ref=Ref.map(LEAVE.TYPE))


def mail_to(l):
    try:
        Mail().to(l)
    except Exception, e:
        log.exception(e)


if __name__ == "__main__":
    pass

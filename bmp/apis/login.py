#coding: utf-8
from flask import session
from bmp.apis.base import BaseApi
from bmp.utils import user_ldap
from bmp.const import USER_SESSION

class LoginApi(BaseApi):
    route="/login/<string:uid>/<string:pwd>"
    def auth(self):
        return True

    def get(self,uid,pwd):
        if session.__contains__(USER_SESSION):
            return self.fail("已登录")

        result,user= user_ldap.auth(uid,pwd)
        if result:
            session[USER_SESSION]=user
            return self.succ(session[USER_SESSION])

        return self.fail("用户名或密码错误")
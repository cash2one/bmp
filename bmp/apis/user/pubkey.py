# coding: utf-8

import rsa
from flask import session

from bmp.apis.base import BaseApi
from bmp.const import KEY_SESSION


class PubkeyApi(BaseApi):
    route = "/login/pubkey"

    def auth(self):
        return True

    def get(self):
        pub, pri = rsa.newkeys(1024)
        session[KEY_SESSION] = {
            "n": pri.n,
            "e": pri.e,
            "d": pri.d,
            "p": pri.p,
            "q": pri.q
        }
        return self.succ({
            "n": hex(pub.n)[2:-1],
            "e": hex(pub.e)[2:]
        })
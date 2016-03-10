# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.idc import Idc_host


class IdcApi(BaseApi):
    route = ["/idc","/idc/<int:iid>", "/idc/<int:page>/<int:pre_page>"]

    def get(self, page, pre_page, iid=None):
        if None != iid:
            return self.succ(Idc_host.get(iid))
        return self.succ(Idc_host.select(page, pre_page))

    def post(self):
        submit = self.request()
        return self.succ(Idc_host.add(submit))

    def delete(self,iid):
        return self.succ(Idc_host.delete(iid))


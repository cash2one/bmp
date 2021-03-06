# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.asset import Icp


class IcpApi(BaseApi):
    route = ["/icp", "/icp/<int:id>"]

    def get(self, id=0):
        if id: self.succ(Icp.get(id))
        return self.succ(Icp.select())

    def post(self):
        submit = self.request()
        Icp.add(submit)
        return self.succ()

    def delete(self):
        submit = self.request()
        Icp.delete(submit["ids"].split(","))
        return self.succ()

    def put(self, id):
        submit = self.request()
        submit["id"] = id
        Icp.edit(submit)
        return self.succ()


if __name__ == "__main__":
    Icp.delete(23)

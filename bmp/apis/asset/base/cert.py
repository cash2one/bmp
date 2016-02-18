# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.asset import Cert


class CertApi(BaseApi):
    route = ["/cert", "/cert/<int:id>"]

    def get(self, id=0):
        if id:self.succ(Cert.get(id))
        return self.succ(Cert.select())

    def post(self):
        submit = self.request()
        return self.succ(Cert.add(submit))

    def delete(self, id):
        Cert.delete(id)
        return self.succ()

    def put(self, id):
        submit=self.request()
        submit["id"]=id
        Cert.edit(submit)
        return self.succ()


if __name__ == "__main__":
    Cert.add({
        "name":"baidu.com",
        "sp":"万网",
        "end_time":"2000-01-01"
    })

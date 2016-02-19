# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.asset import Contract
from bmp.tasks.mail.asset.contract import Mail


class ContractApi(BaseApi):
    route = ["/contract", "/contract/<int:id>"]

    def get(self, id=0):
        if id:
            return self.succ(Contract.get(id))
        return self.succ(Contract.select())

    def post(self):
        submit = self.request()
        contract = Contract.add(submit)
        Mail().to(contract)
        return self.succ()

    def delete(self, id):
        Contract.delete(id)
        return self.succ()

    def put(self, id):
        submit = self.request()
        Contract.edit(id, submit)
        return self.succ()


if __name__ == "__main__":
    pass

# coding=utf-8
from datetime import datetime

from bmp.apis.base import BaseApi
from bmp.models.report import Report
from datetime import datetime
from datetime import timedelta

class ReportApi(BaseApi):
    route = [
        "/report",
        "/report/<string:year>/<string:weeks>",
        "/report/<string:year>/<string:weeks>/<int:team_id>",
        "/report/<int:rid>"
    ]

    def get(self,year,weeks,team_id=None):
        dt=datetime(year,1,1)+timedelta(weeks=weeks)
        beg_time=dt-timedelta(days=dt.weekday())
        end_time=(dt+timedelta(days=6-dt.weekday())).replace(hour=23,minute=59,second=59)
        return Report.select(_filters=[Report.create_time.between(beg_time,end_time)])


    def post(self):
        submit = self.request()

        Report.add(submit)
        return self.succ()

    def delete(self, rid):
        Report.delete(rid)
        return self.succ()

    def put(self, rid):
        submit = self.request()
        submit["id"] = rid
        Report.edit(submit)
        return self.succ()


if __name__ == "__main__":
    report=Report.add({"schedule":"test","create_time":""})

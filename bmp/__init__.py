#coding: utf-8
from myapp import Myapp

app = Myapp.get_instance(__name__)
db=app.db
log=app.logger

app.add_view_rule("index")
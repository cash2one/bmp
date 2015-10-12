from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter
from utils import path

import sys
import re


class _RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        BaseConverter.__init__(self,map)
        self.regex = args[0]


class Myapp(Flask):
    __app=None
    @staticmethod
    def get_instance(name):
        if Myapp.__app==None:
            Myapp.__app=Myapp(name)
        return Myapp.__app

    @staticmethod
    def __to_dict(self):
        print(self.__table__.columns)
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def __init__(self,name):
        Flask.__init__(self,name)
        if not self.debug:
            self.config.from_object("bmp.config.Config")
        else:
            self.config.from_object("bmp.config.DebugConfig")

        self.db=SQLAlchemy(self)
        self.db.text_factory = str

        self.db.Model.to_dict=self.__to_dict

        self.url_map.converters["regex"] = _RegexConverter

    def __add_api_rule(self,module):
        self.__add_rule("bmp.apis.%s"%module,"Api",
                        methods=["GET","POST","PUT","DELETE"],
                        root="/apis/%s"%self.config["API_VERSION"])

    def add_view_rule(self,module):
        self.__add_rule("bmp.views.%s"%module,"View",methods=["GET"])

    def __add_rule(self,module,suffix,methods,root=""):
        #bmp.views.index
        '''
        from bmp.views.index import IndexView
        app.add_url_rule("/",view_func=IndexView.as_view("index"))
        '''
        cls_name=module.split(".")[-1]

        exec("import %s"%(module))

        cls_name=cls_name.capitalize()+suffix
        if not hasattr(sys.modules[module],cls_name):
            return
        cls=getattr(sys.modules[module],cls_name)
        if not hasattr(cls,"route"):
            return

        if not isinstance(cls.route,list):
            route=root+cls.route
            self.add_url_rule(route,view_func=cls.as_view(route),methods=methods)
        else:
            for route in cls.route:
                route=root+route
                self.add_url_rule(route,view_func=cls.as_view(route),methods=methods)

    def run(self, host=None, port=None, debug=None, **options):
        apis="%s/apis"%self.root_path.replace("\\","/")
        regx=re.compile(r"^%s/(.+)\.py$"%apis)
        for name in path.files(apis,".+\.py$"):
            mod=regx.findall(name.replace("\\","/"))[0].replace("/",".")
            self.__add_api_rule(mod)

        super(Myapp,self).run(host,port,debug,**options)

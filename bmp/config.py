#coding=utf-8
import os
from datetime import timedelta

class Config(object):
    LDAP_HOST = "ldap://ldap.chinascopefinancial.com"
    LDAP_PORT = "389"
    LDAP_ACCOUNT = "cn=emp_user,dc=employees,dc=acl,dc=people,dc=chinascopefinancial,dc=com"#"cn=admin,dc=chinascopefinancial,dc=com"
    LDAP_PASSWORD = "\X'94ORKWV#4gCyHFzPV"#"nfUa5gCxXzUNs9ybM8ko"
    LDAP_BASE_DN = "dc=chinascopefinancial,dc=com"

    SQLALCHEMY_DATABASE_URI="mysql://ops:Ops@192.168.250.10:3306/bmp"
    SQLALCHEMY_TRACK_MODIFICATIONS=True

    SECRET_KEY="scope"#os.urandom(1024)
    SESSION_TYPE="filesystem"
    PERMANENT_SESSION_LIFETIME=timedelta(days=7)

    API_VERSION="v1.0"

    MAIL_SERVER = "mail.chinascopefinancial.com"
    MAIL_USERNAME = "ops@chinascopefinancial.com"
    MAIL_PASSWORD = "GmgW3UXF"
    MAIL_DEFAULT_SENDER="ops@chinascopefinancial.com"

    LOG_PATH="bmp.log"
    LOG_MAX=""

    UPLOAD_FOLDER="/upload"

    HOST=""
    PORT=5000


class Test(Config):
    SQLALCHEMY_DATABASE_URI="mysql://ops:Ops@192.168.250.10:3306/bmp"
    HOST = "192.168.0.143"

class Dev(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://ops:Ops@192.168.250.10:3306/bmp"
    HOST = "192.168.0.143"

class Testserver(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://ops:Ops@192.168.250.10:3306/bmp"
    HOST = "127.0.0.1"

class Yutest(Config):
    HOST = "192.168.0.57"
    SQLALCHEMY_DATABASE_URI="mysql://ops:Ops@192.168.250.10:3306/test"
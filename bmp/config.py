# coding=utf-8
from datetime import timedelta


class Config(object):
    LDAP_HOST = "ldap://ldap.chinascopefinancial.com"
    LDAP_PORT = "389"
    LDAP_ACCOUNT = "cn=emp_admin,dc=employees,dc=acl,dc=people,dc=chinascopefinancial,dc=com"#"cn=emp_user,dc=employees,dc=acl,dc=people,dc=chinascopefinancial,dc=com"
    LDAP_PASSWORD = "IVXM6e7cT\"CC9bua!BXO"#"\X'94ORKWV#4gCyHFzPV"
    LDAP_BASE_DN = "dc=employees,dc=people,dc=chinascopefinancial,dc=com"#"dc=chinascopefinancial,dc=com"

    SQLALCHEMY_DATABASE_URI = "mysql://ops:Ops@192.168.250.10:3306/bmp"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    ADA_FD_URI = "mysql://ops_view:ops_view@122.144.134.21:3306/ada-fd"

    SECRET_KEY = "scope"  # os.urandom(1024)
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    API_VERSION = "v1.0"

    MAIL_SERVER = "mail.chinascopefinancial.com"
    MAIL_USERNAME = "ops@chinascopefinancial.com"
    MAIL_PASSWORD = "GmgW3UXF"
    MAIL_DEFAULT_SENDER = "ops@chinascopefinancial.com"
    MAIL_ALERT = "it@chinascopefinancial.com"

    LOG_PATH = "bmp.log"
    LOG_MAX = ""

    UPLOAD_FOLDER = "/static/upload"
    SINGLETON = True
    HOST = ""
    PORT = 5000
    MAX_CONTENT_LENGTH = 1 * 1023 * 1024 * 1024
    DOMAIN = "http://ops.chinascope.net/"
    SSH_HOST="122.144.134.95"
    SSH_USER = "depops"
    SSH_PASSWORD = "Vulooz5S"

    SSH_IDC_HOST="192.168.250.254"
    SSH_IDC_USER = "opsUser"
    SSH_IDC_PASSWORD = "chin@sc0pe321"

    SMS_GATEWAY = "http://106.ihuyi.cn/webservice/sms.php?method=Submit"
    SMS_USER = "cf_chinascope"
    SMS_PASSWORD = "zKqVjm"

    MONGO_HR_HOST = "122.144.134.3"
    MONGO_HR_DATABASE = "ichinascope"


class Test(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://ops:Ops@192.168.250.10:3306/bmp_test"
    HOST = "localhost"
    MAIL_ALERT = "chenglong.yan@chinascopefinancial.com"
    SSH_HOST = "192.168.250.253"
    SSH_USER = "depops"
    SSH_PASSWORD = "Passwd@!"

    SSH_IDC_HOST = "192.168.250.253"
    SSH_IDC_USER = "depops"
    SSH_IDC_PASSWORD = "Passwd@!"

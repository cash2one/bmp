
class Config(object):
    LDAP_HOST = "ldap://ldap.chinascopefinancial.com"
    LDAP_PORT = "389"
    LDAP_ACCOUNT = "cn=emp_user,dc=employees,dc=acl,dc=people,dc=chinascopefinancial,dc=com"#"cn=admin,dc=chinascopefinancial,dc=com"
    LDAP_PASSWORD = "\X'94ORKWV#4gCyHFzPV"#"nfUa5gCxXzUNs9ybM8ko"
    LDAP_BASE_DN = "dc=chinascopefinancial,dc=com"

    SQLALCHEMY_DATABASE_URI="sqlite:////test.db"

    SECRET_KEY="scope"
    SESSION_TYPE="filesystem"

    API_VERSION="v1.0"

    MAIL_SERVER = "mail.chinascopefinancial.com"
    MAIL_PORT = 110
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = "ops@chinascopefinancial.com"
    MAIL_PASSWORD = "GmgW3UXF"

class DebugConfig(Config):
    SQLALCHEMY_DATABASE_URI = ""
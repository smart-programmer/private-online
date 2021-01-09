import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLITE_VARIABLE = 'sqlite:///'

class Config:
    SECRET_KEY = "AAA2002AAA"
    SQLALCHEMY_DATABASE_URI = SQLITE_VARIABLE + os.path.join(basedir, 'sqlite.db') # NOTE: the flask migration moudle/package database url must be relative to the file that will be run when migrating: https://stackoverflow.com/questions/57758213/unable-to-find-source-of-error-root-error-cant-locate-revision-identified-b 
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'horizonlighttrainingcentre@gmail.com'
    MAIL_PASSWORD = "ofzwnsduwbjwylea"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class Production_Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
import os

class Config:
    SECRET_KEY = "AAA2002AAA"
    SQLALCHEMY_DATABASE_URI = "sqlite:///../sqlite.db" # NOTE: the flask migration moudle/package database url must be relative to the file that will be run when migrating of
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'webdevcompany123@gmail.com'
    MAIL_PASSWORD = "oddirclaonixpurg"
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
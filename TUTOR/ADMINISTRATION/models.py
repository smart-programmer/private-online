from flask import current_app
from TUTOR import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from datetime import datetime


# class TUTORModel(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), nullable=False)
#     number_of_players = db.Column(db.Integer, nullable=False) # centimeters
   
#     def __repr__(self):
#         return f"{self.name} | {self.number_of_players}"



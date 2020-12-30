from TUTOR import db




class TutorDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_accepted = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, nullable=False)
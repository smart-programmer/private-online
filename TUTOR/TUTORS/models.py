from TUTOR import db





class TutorDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_accepted = db.Column(db.Boolean, nullable=False, default=False)
    courses = db.relationship('CourseModel', backref='tutor', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'),
        nullable=False)

    
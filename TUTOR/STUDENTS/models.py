from TUTOR import db
from TUTOR.ADMINISTRATION.models import courses
from datetime import datetime





class StudentDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(300), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'),
        nullable=False)
    courses = db.relationship('CourseModel', secondary=courses, lazy='subquery',
        backref=db.backref('students', lazy=True))



    def age(self):
        return int((datetime.date(datetime.utcnow()) - datetime.date(self.date_of_birth)).days / 365)
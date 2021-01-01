from flask import current_app
from TUTOR import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from datetime import datetime





@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

class UserModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(30), nullable=False)
    email_confirmation_code = db.Column(db.String(5), nullable=True)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    admin_data_model = db.relationship('AdminDataModel', backref='user', uselist=False)
    tutor_data_model = db.relationship('TutorDataModel', backref='user', uselist=False)
    student_data_model = db.relationship('StudentDataModel', backref='user', uselist=False)

    # The Default Expire Time is Equal to 30 Mins

    def full_name(self):
        return self.first_name + " " + self.last_name

    def age(self):
        return int((datetime.date(datetime.utcnow()) - datetime.date(self.date_of_birth)).days / 365)

    def get_reset_token(self, expire_seconds=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expire_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return UserModel.query.get(user_id)

    def get_email_change_token(self, new_email, expire_seconds=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expire_seconds)
        return s.dumps({'user_id': self.id, 'user_email': new_email}).decode('utf-8')

    @staticmethod
    def verify_email_change_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        try:
            user_email = s.loads(token)['user_email']
        except:
            return None
        
        return UserModel.query.get(user_id), user_email


    def __repr__(self):
        return f"{self.full_name()}"



courses = db.Table('courses',
    db.Column('course_model_id', db.Integer, db.ForeignKey('course_model.id'), primary_key=True),
    db.Column('student_data_model_id', db.Integer, db.ForeignKey('student_data_model.id'), primary_key=True)
)



class AdminDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))



class CourseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor_data_model.id'),
        nullable=False)


class TutorDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_accepted = db.Column(db.Boolean, nullable=False, default=False)
    courses = db.relationship('CourseModel', backref='tutor', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))


class StudentDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(300), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    courses = db.relationship('CourseModel', secondary=courses, lazy='subquery',
        backref=db.backref('students', lazy=True))



    def age(self):
        return int((datetime.date(datetime.utcnow()) - datetime.date(self.date_of_birth)).days / 365)




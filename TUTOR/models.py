from flask import current_app
from TUTOR import db, login_manager, create_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from datetime import datetime
import json

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
    _gender = db.Column(db.Boolean, nullable=False, default=True)
    email_confirmation_code = db.Column(db.String(5), nullable=True)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    admin_data_model = db.relationship('AdminDataModel', backref='user', uselist=False)
    tutor_data_model = db.relationship('TutorDataModel', backref='user', uselist=False)
    student_data_model = db.relationship('StudentDataModel', backref='user', uselist=False)

    # The Default Expire Time is Equal to 30 Mins

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

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

    @property
    def gender(self):
        return "male" if self._gender else "female"


    def __repr__(self):
        return f"{self.full_name}"



courses = db.Table('courses',
    db.Column('course_model_id', db.Integer, db.ForeignKey('course_model.id'), primary_key=True),
    db.Column('student_data_model_id', db.Integer, db.ForeignKey('student_data_model.id'), primary_key=True)
)



class AdminDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))



class CourseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(130), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    subject = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    min_students = db.Column(db.Integer, nullable=False) 
    max_students = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    began = db.Column(db.Boolean, nullable=False, default=False)
    ended = db.Column(db.Boolean, nullable=False, default=False)
    course_type = db.Column(db.Integer, nullable=False) # 1 for start when min number # 2 for start with min and date
    _period = db.Column(db.Integer, nullable=True) # days
    _start_date = db.Column(db.DateTime, nullable=True)
    _end_date = db.Column(db.DateTime, nullable=True)
    links = db.Column(db.String(), nullable=False) # {"zoom": "link", ....}
    weekly_time_table_json  = db.Column(db.String(1000), nullable=False) # {"saturday": {"from": ..., "to": ...}, ...}
    created_by_admin = db.Column(db.Boolean, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tutor_data_model_id = db.Column(db.Integer, db.ForeignKey('tutor_data_model.id'),
        nullable=False)


    @property
    def period(self):
        return self._period if self._period else int((datetime.date(self._end_date) - datetime.date(self._start_date)).days)

    @property
    def weekly_time_table(self):
        return json.loads(self.weekly_time_table_json)

    @property
    def start_date(self):
        return "يبدأ عند اكتمال الطلاب" if self._start_date == None else datetime.date(self._start_date)

    @property
    def end_date(self):
        return f"ينتهي بعد {self.period} ايام من بدأ الدورة" if self._end_date == None else datetime.date(self._end_date)

    @property
    def number_of_participants(self):
        return len(self.students)
    
    @property
    def empty_seats(self):
        return self.max_students - self.number_of_participants

    @property
    def state(self):
        if not self.began:
            return "لم تبدأ بعد"
        elif not sel.ended:
            return "قائم"
        else:
            return "انتهى"

    @staticmethod
    def is_allowed_to_control_course(course, user):
        user_type = user.user_type
        if not user_type == "student":
            allow_tutors_edit_course_setting = SiteSettingsModel.instance().allow_tutors_to_edit_courses["setting_value"]
            if user_type == "tutor":
                if not allow_tutors_edit_course_setting:
                    return False
                else:
                    if user == course.tutor.user:
                        return True
                    else:
                        return False
            else:
                return True
        else:
            return False

    @staticmethod
    def is_allowed_to_create_course(course, user):
        user_type = user.user_type
        if not user_type == "student":
            allow_tutors_to_create_courses = SiteSettingsModel.instance().allow_tutors_to_create_courses["setting_value"]
            if user_type == "tutor":
                if not allow_tutors_edit_course_setting:
                    return False
                else:
                    if user == course.tutor.user:
                        return True
                    else:
                        return False
            else:
                return True
        else:
            return False


class TutorDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    nationality = db.Column(db.String(30), nullable=False)
    qualification = db.Column(db.String(35), nullable=False)
    major = db.Column(db.String(35), nullable=False)
    current_job = db.Column(db.String(50), nullable=False)
    _subjects = db.Column(db.String(), nullable=False) # [subject1, subject2, ...]
    years_of_experience = db.Column(db.Integer, nullable=False)
    _tools_used_for_online_tutoring = db.Column(db.String(), nullable=False) # [tool1, tool2, ...]
    is_accepted = db.Column(db.Boolean, nullable=False, default=False)
    courses = db.relationship('CourseModel', backref='tutor')
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    @property
    def age(self):
        return int((datetime.date(datetime.utcnow()) - datetime.date(self.date_of_birth)).days / 365)

    @property
    def subjects(self):
        return json.loads(self._subjects)
        # return self._subjects.split(",")
        
    @property
    def tools_used_for_online_tutoring(self):
        return json.loads(self._tools_used_for_online_tutoring)
        # return self._tools_used_for_online_tutoring.split(",")

    @staticmethod
    def list_to_comma_seperated_string(ls):
        str_ls = str(ls)
        str_ls = str_ls.replace(str_ls[0], " ")
        str_ls = str_ls.replace(str_ls[-1], " ")
        new_ls = str_ls.strip().split(",")
        n = None
        for item in new_ls:
            n = item.strip()
            n = str_ls.replace(str_ls[1], "")
            n = str_ls.replace(str_ls[-2], "")
        return n.strip()
    




class StudentDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    courses = db.relationship('CourseModel', secondary=courses, lazy='subquery',
        backref=db.backref('students', lazy=True))


    @property
    def age(self):
        return int((datetime.date(datetime.utcnow()) - datetime.date(self.date_of_birth)).days / 365)





class SiteSettingsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _settings = db.Column(db.String(), nullable=True) # '{"setting_name": {"setting_type": ..., "setting_value": ....}, ....}'
    # name = db.Column(db.String(50), nullable=False)
    # value = db.Column(db.String(50), nullable=False)
    # allowe_tutors_to_edit_courses = db.Column(db.Boolean, nullable=False, default=False)
    # allow_tutors_to_create_courses = db.Column(db.Boolean, nullable=False, default=False)


    @property
    def allow_tutors_to_edit_courses(self):
        return self.settings["allow_tutors_to_edit_courses"]

    @property
    def allow_tutors_to_create_courses(self):
        return self.settings["allow_tutors_to_create_courses"]

    @property
    def subjects(self):
        return self.settings["subjects"]

    @property
    def settings(self):
        return json.loads(self._settings)

    def add_or_change_setting(self, setting_key, setting_value):
        settings_dict = self.settings
        settings_dict[setting_key]["setting_value"] = setting_value
        self._settings = json.dumps(settings_dict)
        db.session.commit()

    def reverse_bool_setting(self, setting_key):
        settings_dict = self.settings
        settings_dict[setting_key]["setting_value"] = not settings_dict[setting_key]["setting_value"]
        self._settings = json.dumps(settings_dict)
        db.session.commit()

    
    def add_to_list_type_setting(self, setting_key, item):
        settings_dict = self.settings
        settings_dict[setting_key]["setting_value"].append(item)
        self._settings = json.dumps(settings_dict)
        db.session.commit() 

    def add_or_change_to_dict_type_setting(self, setting_key, key, value):
        setting = self.settings[setting_key]["setting_value"]
        setting[key] = value
        self._settings[setting_key]["setting_value"] = json.dumps(setting)
        db.session.commit() 

    @classmethod
    def instance(cls):
        return cls.query.get(1)

    # @staticmethod
    # def get_str_bool(string):
    #     return True if string in ("True", "true") else False

    # @classmethod
    # def get_settings_dict(cls):
    #     all_settings = cls.query.all()
    #     settings = {}
    #     for setting in all_settings:
    #         if setting.is_bool():
    #             settings[setting.name] = SiteSettingsModel.get_str_bool(setting.value)
    #         else: 
    #             settings[setting.name] = setting.value
    #     return settings




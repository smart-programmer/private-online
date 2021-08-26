from flask_wtf import FlaskForm
import wtforms
from wtforms.fields.html5 import DateField, IntegerField, IntegerRangeField, DecimalRangeField, DecimalField
from wtforms.validators import DataRequired, length, Email, ValidationError, EqualTo, Optional
from wtforms_components import SelectField
from flask_wtf.file import FileField, FileAllowed 
from wtforms.widgets import TextArea
from TUTOR.models import UserModel, SiteSettingsModel
from flask_login import current_user
from TUTOR import bcrypt
from TUTOR.utils.utils import dict_to_select_compatable_tuple
from TUTOR.settings import CURRENCIES
from datetime import datetime
import json


genders = [
    ("1", "male"),
    ("0", "female")
]

class TutorRegistrationForm(FlaskForm):
    first_name = wtforms.StringField("first name", validators=[length(max=128), DataRequired()])
    last_name = wtforms.StringField("last name", validators=[length(max=128), DataRequired()])
    username = wtforms.StringField("username", validators=[length(max=20), DataRequired()])
    email = wtforms.StringField("email", validators=[length(min=3, max=255), DataRequired()])
    gender = wtforms.SelectField("gender", choices=genders, validators=[DataRequired()])
    date_of_birth = DateField("age", format="%Y-%m-%d", validators=[DataRequired()])
    nationality = wtforms.StringField("nationality", validators=[length(max=30), DataRequired()])
    qualification = wtforms.StringField("qualification", validators=[length(max=35), DataRequired()])
    major = wtforms.StringField("major", validators=[length(max=35), DataRequired()])
    current_job = wtforms.StringField("current job", validators=[length(max=50), DataRequired()])
    subjects = wtforms.StringField("subjects you want to teach") # wtforms.SelectField("subjects you want to teach", choices=(()), validators=[length(min=0, max=30)])
    years_of_experience = IntegerField("years of experience", validators=[DataRequired()], render_kw={"min": 0, "max": 100})
    tools_used_for_online_tutoring = wtforms.StringField("tools used for online tutoring", validators=[length(min=0, max=60)])
    password = wtforms.PasswordField("password", validators=[length(min=3, max=40), DataRequired()])
    confirm_password = wtforms.PasswordField("confirm password", validators=[length(min=3, max=40), DataRequired(), EqualTo("password")])
    user_agreement = wtforms.BooleanField("accept user agreement", validators=[DataRequired()])
    privacy_use_agreement = wtforms.BooleanField("privacy and use agreement", validators=[DataRequired()])
    submit = wtforms.SubmitField("Register")

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("username already taken")

    def validate_user_agreement(self, user_agreement):
        if not user_agreement.data:
            raise ValidationError("you have to accept our user agreement")

    def validate_privacy_use_agreement(self, privacy_use_agreement):
        if not privacy_use_agreement.data:
            raise ValidationError("you have to accept our privacy and use agreement")

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("this email is already registered, did you forget your password?")

    def validate_subjects(self, subjects):
        settings_subjects = SiteSettingsModel.instance().subjects["setting_value"]
        subjects_list = None
        try:
            subjects_list = json.loads(subjects.data)
        except:
            raise ValidationError("not a valid json object")
        finally:
            if not type(subjects_list).__name__ == "list":
                raise ValidationError(subjects_list)
            for i in subjects_list:
                count = subjects_list.count(i)
                if count > 1:
                    raise ValidationError(f"{i} is repeated {count} times")
                if settings_subjects.count(i) < 1:
                    raise ValidationError(f"{i} is not a subject")
            

    def validate_tools_used_for_online_tutoring(self, tools_used_for_online_tutoring):
        tools_used_for_online_tutoring_list = None
        try:
            tools_used_for_online_tutoring_list = json.loads(tools_used_for_online_tutoring.data)
        except:
            raise ValidationError("not a valid json object")
        finally:
            if not type(tools_used_for_online_tutoring_list).__name__ == "list":
                raise ValidationError("not a list")


class TutorEditProfileForm(FlaskForm):
    first_name = wtforms.StringField("first name", validators=[length(max=128), DataRequired()])
    last_name = wtforms.StringField("last name", validators=[length(max=128), DataRequired()])
    username = wtforms.StringField("username", validators=[length(max=20), DataRequired()])
    email = wtforms.StringField("email", validators=[length(min=3, max=255), DataRequired()])
    gender = wtforms.SelectField("gender", choices=genders, validators=[DataRequired()])
    date_of_birth = DateField("age", format="%Y-%m-%d", validators=[DataRequired()])
    nationality = wtforms.StringField("nationality", validators=[length(max=30), DataRequired()])
    qualification = wtforms.StringField("qualification", validators=[length(max=35), DataRequired()])
    major = wtforms.StringField("major", validators=[length(max=35), DataRequired()])
    current_job = wtforms.StringField("current job", validators=[length(max=50), DataRequired()])
    subjects = wtforms.StringField("subjects you want to teach")
    years_of_experience = IntegerField("years of experience", validators=[DataRequired()], render_kw={"min": 0, "max": 100})
    tools_used_for_online_tutoring = wtforms.StringField("tools used for online tutoring", validators=[length(min=0, max=60)])
    submit = wtforms.SubmitField("Edit")

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user and user != current_user:
            raise ValidationError("username already taken")

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user and user != current_user:
            raise ValidationError("this other email is already registered, did you forget your password?")


currencies = dict_to_select_compatable_tuple(CURRENCIES)
course_types = (
    [
        "1", "دورة تبدأ عند الوصول للحد الادنى من المتسجلين بدون وجود تاريخ بداية"
    ],
    [
        "2", "دورة تبدأ عند تاريخ معين عند وصول للحد الادنى من المتسجلين"
    ],
    [
        None, "----"
    ]
)

class CourseCreationForm(FlaskForm):
    name = wtforms.StringField("course name", validators=[length(max=130), DataRequired()])
    description = wtforms.StringField("description", validators=[length(max=1000), DataRequired()], widget=TextArea())
    price = IntegerField("price", validators=[DataRequired()])
    subject = wtforms.SelectField("course subject", choices=(()), validators=[DataRequired()])
    course_type = wtforms.SelectField("course type", choices=course_types, default=None, validators=[DataRequired()])
    currency = wtforms.SelectField("currency", choices=currencies, validators=[DataRequired()])
    period = IntegerField("period", validators=[Optional()])
    start_date = DateField("start date", format="%Y-%m-%d", validators=[Optional()])
    end_date = DateField("end date", format="%Y-%m-%d", validators=[Optional()])
    zoom_link = wtforms.StringField("zoom link", validators=[length(max=255), DataRequired()], widget=TextArea()) 
    min_students = IntegerField("minimum number of students", validators=[DataRequired()])
    max_students = IntegerField("maximum number of students", validators=[Optional()])
    saturday_start = DecimalField("saturday class start time", validators=[Optional()], render_kw={"min": 1, "max": 24})
    saturday_end = DecimalField("saturday class end time", validators=[Optional()], render_kw={"min": 1, "max": 24})
    sunday_start = DecimalField("sunday class start time", validators=[Optional()], render_kw={"min": 1, "max": 24})
    sunday_end = DecimalField("sunday class end time", validators=[Optional()], render_kw={"min": 1, "max": 24})
    monday_start = DecimalField("monday class start time", validators=[Optional()], render_kw={"min": 1, "max": 24})
    monday_end = DecimalField("monday class end time", validators=[Optional()], render_kw={"min": 1, "max": 24})
    tuesday_start = DecimalField("tuesday class start time", validators=[Optional()], render_kw={"min": 1, "max": 24})
    tuesday_end = DecimalField("tuesday class end time", validators=[Optional()], render_kw={"min": 1, "max": 24})
    wednesday_start = DecimalField("wednesday class start time", validators=[Optional()], render_kw={"min": 1, "max": 24})
    wednesday_end = DecimalField("wednesday class end time", validators=[Optional()], render_kw={"min": 1, "max": 24})
    thursday_start = DecimalField("thursday class start time", validators=[Optional()], render_kw={"min": 1, "max": 24})
    thursday_end = DecimalField("thursday class end time", validators=[Optional()], render_kw={"min": 1, "max": 24})
    friday_start = DecimalField("friday class start time", validators=[Optional()], render_kw={"min": 1, "max": 24})
    friday_end = DecimalField("friday class end time", validators=[Optional()], render_kw={"min": 1, "max": 24})
    submit = wtforms.SubmitField("create course")


    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if self.course_type == 1 and self.start_date.data and self.end_date.data:
            raise ValidationError("لا يمكن اذافة تاريخ في هذا النوع من الدورات")

        if self.course_type == 2 and self.period.data:
            raise ValidationError("لا يمكن اضافة مدة دورة في هذ االنوع من الدورات")

        if self.start_date.data and self.end_date.data:
            period = int((self.end_date.data - self.start_date.data).days)
            if period <= 0:
                raise ValidationError("تأكد من الفارق بين تاريخ البداية والنهاية")

        if self.course_type.data == 2 and not self.max_students.data:
            raise ValidationError("يجب وضع اقصى عدد طلاب اذااردت هذا النوع من الدورات")

        if self.course_type.data == 2:
            if self.max_students.data < self.min_students.data:
                raise ValidationError("يجب ان يكون الحد الادنى اقل او مساو للحد الاعلى")


        return True

    def validate_start_date(self, start_date):
        if start_date:
            delta_time = int((start_date.data - datetime.date(datetime.utcnow())).days)
            if delta_time <= 0 and start_date.data != datetime.date(datetime.utcnow()):
                raise ValidationError("الرجاء التأكد من تاريخ البداية")
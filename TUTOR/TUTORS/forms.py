from flask_wtf import FlaskForm
import wtforms
from wtforms.fields.html5 import DateField, IntegerField, IntegerRangeField, DecimalRangeField, DecimalField
from wtforms.validators import DataRequired, length, Email, ValidationError, EqualTo, Optional
from wtforms_components import SelectField
from flask_wtf.file import FileField, FileAllowed 
from wtforms.widgets import TextArea
from TUTOR.models import UserModel
from flask_login import current_user
from TUTOR import bcrypt
from TUTOR.utils.utils import dict_to_select_compatable_tuple
from TUTOR.settings import CURRENCIES


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
    subjects = wtforms.StringField("subject you want to teach", validators=[length(min=0, max=30)])
    years_of_experience = IntegerField("years of experience", validators=[DataRequired()], render_kw={"min": 0, "max": 100})
    tools_used_for_online_tutoring = wtforms.StringField("tools used for online tutoring", validators=[length(min=0, max=60)])
    password = wtforms.StringField("password", validators=[length(min=3, max=40), DataRequired()])
    confirm_password = wtforms.StringField("confirm password", validators=[length(min=3, max=40), DataRequired(), EqualTo("password")])
    submit = wtforms.SubmitField("Register")

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("username already taken")

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("this email is already registered, did you forget your password?")


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
    subjects = wtforms.StringField("subject you want to teach", validators=[length(min=0, max=30)])
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
subjects = (())

class CourseCreationForm(FlaskForm):
    name = wtforms.StringField("course name", validators=[length(max=130), DataRequired()])
    description = wtforms.StringField("description", validators=[length(max=1000), DataRequired()], widget=TextArea())
    subject = wtforms.SelectField("course subject", choices=subjects, validators=[DataRequired()])
    price = IntegerField("price", validators=[DataRequired()])
    currency = wtforms.SelectField("currency", choices=currencies, validators=[DataRequired()])
    min_students = IntegerField("minimum number of students", validators=[DataRequired()])
    max_students = IntegerField("maximum number of students", validators=[DataRequired()])
    submit = wtforms.SubmitField("create course")
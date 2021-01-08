from flask_wtf import FlaskForm
import wtforms
from wtforms.fields.html5 import DateField, IntegerField, IntegerRangeField, DecimalRangeField, DecimalField
from wtforms.validators import DataRequired, length, Email, ValidationError, EqualTo, Optional
from wtforms_components import SelectField
from flask_wtf.file import FileField, FileAllowed 
from wtforms.widgets import TextArea
from flask_login import current_user
from TUTOR.models import UserModel


genders = [
    ("1", "male"),
    ("0", "female")
]

class StudentRegistrationForm(FlaskForm):
    first_name = wtforms.StringField("first name", validators=[length(max=128), DataRequired()])
    last_name = wtforms.StringField("last name", validators=[length(max=128), DataRequired()])
    username = wtforms.StringField("username", validators=[length(max=20), DataRequired()])
    email = wtforms.StringField("email", validators=[length(min=3, max=255), DataRequired()])
    password = wtforms.StringField("password", validators=[length(min=3, max=40), DataRequired()])
    confirm_password = wtforms.StringField("confirm password", validators=[length(min=3, max=40), DataRequired(), EqualTo("password")])
    school_name = wtforms.StringField("School name", validators=[length(max=300)])
    gender = wtforms.SelectField("gender", choices=genders, validators=[DataRequired()])
    date_of_birth = DateField("age", format="%Y-%m-%d", validators=[DataRequired()])
    submit = wtforms.SubmitField("Register")

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("username already taken")

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("this email is already registered, did you forget your password?")



class StudentEditProfileForm(FlaskForm):
    first_name = wtforms.StringField("first name", validators=[length(max=128), DataRequired()])
    last_name = wtforms.StringField("last name", validators=[length(max=128), DataRequired()])
    username = wtforms.StringField("username", validators=[length(max=20), DataRequired()])
    email = wtforms.StringField("email", validators=[length(min=3, max=255), DataRequired()])
    school_name = wtforms.StringField("School name", validators=[length(max=300)])
    date_of_birth = DateField("age", format="%Y-%m-%d", validators=[DataRequired()])
    gender = wtforms.SelectField("gender", choices=genders, validators=[DataRequired()])
    submit = wtforms.SubmitField("Edit")

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user and user != current_user:
            raise ValidationError("username already taken")

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user and user != current_user:
            raise ValidationError("this other email is already registered, did you forget your password?")



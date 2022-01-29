from flask_wtf import FlaskForm
import wtforms
from wtforms.fields.html5 import DateField, IntegerField, IntegerRangeField, DecimalRangeField, DecimalField
from wtforms.validators import DataRequired, length, Email, ValidationError, EqualTo, Optional
from wtforms_components import SelectField
from flask_wtf.file import FileField, FileAllowed 
from wtforms.widgets import TextArea
from flask_login import current_user
from TUTOR.models import UserModel
from TUTOR.utils.passwords import main_password_policy


genders = [
    ("1", "ذكر"),
    ("0", "انثى")
]

class StudentRegistrationForm(FlaskForm):
    first_name = wtforms.StringField("first name", validators=[length(max=128), DataRequired()])
    last_name = wtforms.StringField("last name", validators=[length(max=128), DataRequired()])
    username = wtforms.StringField("username", validators=[length(max=20), DataRequired()])
    email = wtforms.StringField("email", validators=[length(min=3, max=255), DataRequired()])
    password = wtforms.PasswordField("password", validators=[length(min=3, max=40), DataRequired()])
    confirm_password = wtforms.PasswordField("confirm password", validators=[length(min=3, max=40), DataRequired(), EqualTo("password", message="خانة تأكيد الرقم السري لا تطابق الرقم السري")])
    gender = wtforms.SelectField("gender", choices=genders, validators=[DataRequired()])
    date_of_birth = DateField("age", format="%Y-%m-%d", validators=[DataRequired()])
    user_agreement = wtforms.BooleanField("accept user agreement", validators=[DataRequired()])
    privacy_use_agreement = wtforms.BooleanField("privacy and use agreement", validators=[DataRequired()])
    submit = wtforms.SubmitField("Register")

    def validate_password(self, password):
        if not main_password_policy.password_accepted(password):
            raise ValidationError("الرقم السري لا يحتوي كل الشروط المطلوبة")

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("اسم المستخدم مأخوذ")

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("البريد الالكتروني مسجل من قبل, هل نسيت الرقم السري؟")

    def validate_user_agreement(self, user_agreement):
        if not user_agreement.data:
            raise ValidationError("يجب ان توافق على الشروط لتكمل")

    def validate_privacy_use_agreement(self, privacy_use_agreement):
        if not privacy_use_agreement.data:
            raise ValidationError("يجب ان توافق على الشروط لتكمل")




class StudentEditProfileForm(FlaskForm):
    first_name = wtforms.StringField("first name", validators=[length(max=128), DataRequired()])
    last_name = wtforms.StringField("last name", validators=[length(max=128), DataRequired()])
    username = wtforms.StringField("username", validators=[length(max=20), DataRequired()])
    email = wtforms.StringField("email", validators=[length(min=3, max=255), DataRequired()])
    date_of_birth = DateField("age", format="%Y-%m-%d", validators=[DataRequired()])
    gender = wtforms.SelectField("gender", choices=genders, validators=[DataRequired()])
    submit = wtforms.SubmitField("Edit")

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user and user != current_user:
            raise ValidationError("اسم المستخدم مأخوذ")

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user and user != current_user:
            raise ValidationError("البريد الالكتروني مسجل من قبل, هل نسيت الرقم السري؟")



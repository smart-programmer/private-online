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
from TUTOR.utils.passwords import main_password_policy

class RegistrationForm(FlaskForm):
    first_name = wtforms.StringField("first name", validators=[length(max=128), DataRequired()])
    last_name = wtforms.StringField("last name", validators=[length(max=128), DataRequired()])
    username = wtforms.StringField("username", validators=[length(max=20), DataRequired()])
    email = wtforms.StringField("email", validators=[length(min=3, max=255), DataRequired()])
    password = wtforms.StringField("password", validators=[length(min=3, max=40), DataRequired()])
    confirm_password = wtforms.StringField("confirm password", validators=[length(min=3, max=40), DataRequired(), EqualTo("password")])
    school_name = wtforms.StringField("School name", validators=[length(max=300)])
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


class ConfirmationCodeForm(FlaskForm):
    code = wtforms.StringField("email", validators=[DataRequired()])
    submit = wtforms.SubmitField("verify")


class LoginForm(FlaskForm):
    username_or_email = wtforms.StringField("username", validators=[length(max=255), DataRequired()])
    password = wtforms.PasswordField("password", validators=[DataRequired()])
    submit = wtforms.SubmitField("Login")

    def validate_username_or_email(self, username_or_email):
        user_email = UserModel.query.filter_by(email=username_or_email.data).first()
        user_username = UserModel.query.filter_by(username=username_or_email.data).first()
        if not user_username and not user_email:
            raise ValidationError("لا يوجد حساب يطابق المعلومات المدخلة")




class EditProfileForm(FlaskForm):
    first_name = wtforms.StringField("first name", validators=[length(max=128), DataRequired()])
    last_name = wtforms.StringField("last name", validators=[length(max=128), DataRequired()])
    username = wtforms.StringField("username", validators=[length(max=20), DataRequired()])
    email = wtforms.StringField("email", validators=[length(min=3, max=255), DataRequired()])
    school_name = wtforms.StringField("School name", validators=[length(max=300)])
    date_of_birth = DateField("age", format="%Y-%m-%d", validators=[DataRequired()])
    submit = wtforms.SubmitField("Edit")

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user and user != current_user:
            raise ValidationError("username already taken")

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user and user != current_user:
            raise ValidationError("this other email is already registered, did you forget your password?")


class RequestResetPasswordForm(FlaskForm):
    username_or_email = wtforms.StringField("username or email", validators=[length(min=3, max=255), DataRequired()])
    submit = wtforms.SubmitField("request reset password")

    def validate_username_or_email(self, username_or_email):
        user_email = UserModel.query.filter_by(email=username_or_email.data).first()
        user_username = UserModel.query.filter_by(username=username_or_email.data).first()
        if not user_username and not user_email:
            raise ValidationError("لا يوجد حساب يطابق المعلومات المدخلة")

class ResetPasswordForm(FlaskForm):
    password = wtforms.StringField("password", validators=[length(min=3, max=40), DataRequired()])
    confirm_password = wtforms.StringField("confirm password", validators=[length(min=3, max=40), DataRequired(), EqualTo("password")])
    submit = wtforms.SubmitField("reset password")

    def validate_password(self, password):
        if not main_password_policy.password_accepted(password):
            raise ValidationError("الرقم السري لا يحتوي كل الشروط المطلوبة")

class ChangePasswordForm(FlaskForm):
    old_password = wtforms.StringField("password", validators=[length(min=3, max=40), DataRequired()])
    new_password = wtforms.StringField("new password", validators=[length(min=3, max=40), DataRequired()])
    confirm_password = wtforms.StringField("confirm password", validators=[length(min=3, max=40), DataRequired(), EqualTo("new_password", message="خانة تأكيد الرقم السري لا تطابق الرقم السري")])
    submit = wtforms.SubmitField("change password")

    def validate_old_password(self, old_password):
        if not bcrypt.check_password_hash(current_user.password, old_password.data):
            raise ValidationError("الرقم السري السابق غير صحيح")

    def validate_password(self, password):
        if not main_password_policy.password_accepted(password):
            raise ValidationError("الرقم السري لا يحتوي كل الشروط المطلوبة")



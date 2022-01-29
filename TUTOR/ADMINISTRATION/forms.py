from flask_wtf import FlaskForm
import wtforms
from wtforms.fields.html5 import DateField, IntegerField, IntegerRangeField, DecimalRangeField, DecimalField
from wtforms.validators import DataRequired, length, Email, ValidationError, EqualTo, Optional
from wtforms_components import SelectField, TimeField
from flask_wtf.file import FileField, FileAllowed 
from wtforms.widgets import TextArea
from TUTOR.models import UserModel
from flask_login import current_user
from TUTOR import bcrypt
from TUTOR.models import UserModel
from TUTOR.utils.utils import dict_to_select_compatable_tuple
from TUTOR.settings import CURRENCIES
import os 
from datetime import datetime



admin_types = (
    ("admin1", "highest privilege"),
    ("admin2", "normal admin")
)






class AdminRegistrationForm(FlaskForm):
    first_name = wtforms.StringField("first name", validators=[length(max=128), DataRequired()])
    last_name = wtforms.StringField("last name", validators=[length(max=128), DataRequired()])
    username = wtforms.StringField("username", validators=[length(max=20), DataRequired()])
    email = wtforms.StringField("email", validators=[length(min=3, max=255), DataRequired()])
    admin_type = wtforms.SelectField("admin type", choices=admin_types, validators=[length(min=3, max=255), DataRequired()])
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


class AdminEditProfileForm(FlaskForm):
    first_name = wtforms.StringField("first name", validators=[length(max=128), DataRequired()])
    last_name = wtforms.StringField("last name", validators=[length(max=128), DataRequired()])
    username = wtforms.StringField("username", validators=[length(max=20), DataRequired()])
    email = wtforms.StringField("email", validators=[length(min=3, max=255), DataRequired()])
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


class AdminCourseCreationForm(FlaskForm):
    name = wtforms.StringField("course name", validators=[length(max=130), DataRequired()])
    description = wtforms.StringField("description", validators=[length(max=1000), DataRequired()], widget=TextArea())
    price = IntegerField("price", validators=[DataRequired()])
    subject = wtforms.SelectField("course subject", choices=(()), validators=[DataRequired()])
    course_type = wtforms.SelectField("course type", choices=course_types, default=None, validators=[DataRequired()])
    currency = wtforms.SelectField("currency", choices=currencies, validators=[DataRequired()])
    period = IntegerField("period", validators=[Optional()])
    start_date = DateField("start date", format="%Y-%m-%d", validators=[Optional()])
    end_date = DateField("end date", format="%Y-%m-%d", validators=[Optional()])
    tutor_zoom_link = wtforms.StringField("tutor zoom link", validators=[length(max=255), DataRequired()], widget=TextArea()) 
    students_zoom_link = wtforms.StringField("students zoom link", validators=[length(max=255), DataRequired()], widget=TextArea()) 
    min_students = IntegerField("minimum number of students", validators=[DataRequired()])
    max_students = IntegerField("maximum number of students", validators=[Optional()])
    saturday_start = TimeField(validators=[Optional()])
    saturday_end = TimeField(validators=[Optional()])
    sunday_start = TimeField(validators=[Optional()])
    sunday_end = TimeField(validators=[Optional()])
    monday_start = TimeField(validators=[Optional()])
    monday_end = TimeField(validators=[Optional()])
    tuesday_start = TimeField(validators=[Optional()])
    tuesday_end = TimeField(validators=[Optional()])
    wednesday_start = TimeField(validators=[Optional()])
    wednesday_end = TimeField(validators=[Optional()])
    thursday_start = TimeField(validators=[Optional()])
    thursday_end = TimeField(validators=[Optional()])
    friday_start = TimeField(validators=[Optional()])
    friday_end = TimeField(validators=[Optional()])
    tutors = wtforms.SelectField("tutor", choices=(()), validators=[DataRequired()])
    submit = wtforms.SubmitField("create course")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if self.course_type == 1 and self.start_date.data and self.end_date.data:
            raise ValidationError("لا يمكن اضافة تاريخ في هذا النوع من الدورات")

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

        
            





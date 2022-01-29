from flask_wtf import FlaskForm
import wtforms
from wtforms.fields.html5 import DateField, IntegerField, IntegerRangeField, DecimalRangeField, DecimalField
from wtforms.validators import DataRequired, length, Email, ValidationError, EqualTo, Optional
from wtforms_components import SelectField, TimeField
from flask_wtf.file import FileField, FileAllowed 
from wtforms.widgets import TextArea
from TUTOR.models import UserModel, SiteSettingsModel
from flask_login import current_user
from TUTOR import bcrypt
from TUTOR.utils.utils import dict_to_select_compatable_tuple
from TUTOR.utils.passwords import main_password_policy
from TUTOR.settings import CURRENCIES
from datetime import datetime
import json


genders = [
    ("1", "ذكر"),
    ("0", "انثى")
]



class TutorRegistrationForm(FlaskForm):
    first_name = wtforms.StringField("first name", validators=[length(max=128), DataRequired(message="من فضلك اخل الاسم الاول")])
    last_name = wtforms.StringField("last name", validators=[length(max=128), DataRequired(message="من فضلك ادخل الاسم الاخير")])
    username = wtforms.StringField("username", validators=[length(max=20), DataRequired(message="من فضلك ادخل اسم المستخدم")])
    email = wtforms.StringField("email", validators=[length(min=3, max=255), DataRequired(message="من فضلك ادخل الايميل")])
    gender = wtforms.SelectField("gender", choices=genders, validators=[DataRequired(message="من فضلك اختر الجنس")])
    date_of_birth = DateField("age", format="%Y-%m-%d", validators=[DataRequired(message="من فضلك ادخل تاريخ الميلاد")])
    nationality = wtforms.StringField("nationality", validators=[length(max=30), DataRequired(message="من فضلك ادخل الجنسية")])
    qualification = wtforms.StringField("qualification", validators=[length(max=35), DataRequired(message="من فضلك ادخل المؤهل")])
    major = wtforms.StringField("major", validators=[length(max=35), DataRequired(message="من فضلك ادخل التخصص")])
    current_job = wtforms.StringField("current job", validators=[length(max=50), DataRequired(message="من فضلك ادخل خانة الوظيفة الحالية")])
    subjects = wtforms.StringField("subjects you want to teach") # wtforms.SelectField("subjects you want to teach", choices=(()), validators=[length(min=0, max=30)])
    years_of_experience = IntegerField("years of experience", validators=[DataRequired(message="من فضلك ادخل سنوات الخبرة")], render_kw={"min": 0, "max": 100})
    tools_used_for_online_tutoring = wtforms.StringField("tools used for online tutoring", validators=[length(min=0, max=60)])
    max_classes_per_day = IntegerField("Maximum classes you can give per day", validators=[DataRequired(message="من فضلك ادخل اقصى عدد حصص تستطيع تدريسها في اليوم")], render_kw={"min": 1, "max": 15})
    min_classes_per_day = IntegerField("Minimum classes you can give per day", validators=[DataRequired(message="من فضلك ادخل اقل عدد حصص يناسبك تدريسها في اليوم")], render_kw={"min": 1, "max": 15})
    most_convenietnt_periods = wtforms.StringField("Most convenient periods to teach")
    password = wtforms.PasswordField("password", validators=[length(min=8, max=40), DataRequired(message="من فضلك أدخل الرقم السري")])
    confirm_password = wtforms.PasswordField("confirm password", validators=[length(min=3, max=40), DataRequired(message="من فضلك أكد الرقم السري"), EqualTo("password", message="خانة تأكيد الرقم السري لا تطابق الرقم السري")])
    user_agreement = wtforms.BooleanField("accept user agreement", validators=[DataRequired(message="يجب ان توافق على الشروط لتكمل")])
    privacy_use_agreement = wtforms.BooleanField("privacy and use agreement", validators=[DataRequired(message="يجب ان توافق على الشروط لتكمل")])
    submit = wtforms.SubmitField("Register")

    def validate_password(self, password):
        if not main_password_policy.password_accepted(password):
            raise ValidationError("الرقم السري لا يحتوي كل الشروط المطلوبة")

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("اسم المستخدم مأخوذ")

    def validate_user_agreement(self, user_agreement):
        if not user_agreement.data:
            raise ValidationError("يجب ان توافق على الشروط لتكمل")

    def validate_privacy_use_agreement(self, privacy_use_agreement):
        if not privacy_use_agreement.data:
            raise ValidationError("يجب ان توافق على الشروط لتكمل")

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("البريد الالكتروني مسجل من قبل, هل نسيت الرقم السري؟")

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
    max_classes_per_day = IntegerField("Maximum classes you can give per day", validators=[DataRequired()], render_kw={"min": 1, "max": 15})
    min_classes_per_day = IntegerField("Minimum classes you can give per day", validators=[DataRequired()], render_kw={"min": 1, "max": 15})
    most_convenietnt_periods = wtforms.StringField("Most convenient periods to teach")
    submit = wtforms.SubmitField("Edit")

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user and user != current_user:
            raise ValidationError("اسم المستخدم مأخوذ")

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user and user != current_user:
            raise ValidationError("البريد الالكتروني مسجل من قبل, هل نسيت الرقم السري؟")


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
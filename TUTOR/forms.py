# from flask_wtf import FlaskForm
# import wtforms
# from wtforms.validators import DataRequired, length, Email
# from wtforms_components import SelectField
# from flask_wtf.file import FileField, FileAllowed 
# from wtforms.widgets import TextArea



# subFilters = (
#     ("logos", "شعارات"),
#     ("brochures", "بروشورات"),
#     ("banner", "بنرات"),
#     ("visualIdentity", "هوية بصرية"),
#     ("folders", "فولدرات"),
# )

# permission_levels = (
#     ("MasterAdmin", "مدير مطْلَق"),
#     ("Admin", "مدير")
# )


# class MessageForm(FlaskForm):
#     full_name = wtforms.StringField(
#         "الاسم ", validators=[length(min=3, max=255)])
#     email = wtforms.StringField("البريد الإلكتروني", validators=[
#                                 Email(), DataRequired(), length(max=255)])
#     subject = wtforms.StringField("عنوان الرسالة", validators=[
#                                   length(min=3, max=255)])
#     content = wtforms.TextAreaField("نص الرسالة ", validators=[
#                                     DataRequired(), length(max=1000)])
#     submit = wtforms.SubmitField("أرسل")


# class LoginForm(FlaskForm):
#     username = wtforms.StringField("اسم المستخدم")
#     password = wtforms.StringField("الرقم السري")
#     submit = wtforms.SubmitField("تسجيل الدخول")


# class UploadImage(FlaskForm):
#     image = FileField("upload image", validators=[FileAllowed(["jpg", "png", "GIF", "jpeg", "gif"]), DataRequired()])
#     title = wtforms.StringField("عنوان الصورة ", validators=[
#                                 DataRequired(), length(min=3, max=255)])
#     description = wtforms.StringField(" وصف الصورة ", validators=[
#         DataRequired(), length(min=3, max=255)], widget=TextArea())
#     url = wtforms.StringField("  رابط للصورة ", validators=[
#         length(max=255)])
#     filters = SelectField("التصنيف", choices=subFilters,
#                           validators=[DataRequired()])
#     submit = wtforms.SubmitField("أرفع")


# class UploadTestimonial(FlaskForm):
#     name = wtforms.StringField(" اسم العميل ", validators=[
#         DataRequired(), length(min=3, max=255)])
#     work = wtforms.StringField("  طبيعة عمله ", validators=[
#         DataRequired(), length(min=3, max=255)])
#     description = wtforms.StringField("   ماقله العميل ", validators=[
#         length(min=3, max=500)], widget=TextArea())

#     submit = wtforms.SubmitField("أرفع")


# class ReplyForm(FlaskForm):
#     subject = wtforms.StringField("عنون الرسالة", validators=[
#         length(max=255)])
#     message = wtforms.TextAreaField("نص الرسالة ", validators=[
#                                     DataRequired(), length(max=1000)])
#     submit = wtforms.SubmitField("أرسل")


# class UserForm(FlaskForm):
#     email = wtforms.StringField("email", validators=[length(min=3, max=255)])
#     full_name = wtforms.StringField("full_name", validators=[length(max=255), DataRequired()])
#     password = wtforms.StringField("password", validators=[length(min=3)])
#     username = wtforms.StringField("username", validators=[DataRequired()])
#     permission = SelectField("permission", choices=permission_levels, validators=[DataRequired()])
#     submit = wtforms.SubmitField("سجل")




# class SimpleForm(FlaskForm):
#     button1 = wtforms.SubmitField("button1")
#     button2 = wtforms.SubmitField("button2")
#     button3 = wtforms.SubmitField("button3")
from flask import Blueprint, render_template, request, redirect, url_for, make_response, flash, current_app
from flask_login import current_user, login_user, logout_user
from TUTOR import db, bcrypt
from TUTOR.ADMINISTRATION.forms import AdminRegistrationForm, AdminCourseCreationForm
from TUTOR.models import StudentDataModel, TutorDataModel, UserModel, AdminDataModel, CourseModel, SiteSettingsModel, PaymentModel, AdminstrationStorageModel
from TUTOR.utils.mail import send_user_confirmation_email, send_user_reset_password_email, send_user_change_password_email, send_email_change_request_email, send_deny_email_change_email, send_tutor_accepted_email
from TUTOR.utils.utils import save_image_locally, delete_image, generate_random_digits, login_required, list_to_select_compatable_tuple, json_list_to_select_compatable_tuple
from TUTOR.settings import ADMIN_TYPES, LANGUAGES
from TUTOR.utils.languages import LngObj
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os
import json


admins_blueprint = Blueprint("admins_blueprint", __name__)

@admins_blueprint.context_processor
def utility_processor():
    return dict(get_language_text=LngObj.get_language_text, get_current_page_language_list=LngObj.get_current_page_language_list, languages=LANGUAGES, admin_types=ADMIN_TYPES, settings=SiteSettingsModel.instance())


@admins_blueprint.route('/admins')
@login_required(ADMIN_TYPES)
def home():
    return render_template("admins/index.html")

@admins_blueprint.route("/admins/control-panel", methods=["GET", "POST"])
@login_required(ADMIN_TYPES)
def control_panel(): 
    # add course *
    # delete course **
    # delete student ***
    # delete tutor ***
    # delete student from course **
    # replace teacher from course  **
    # accept tutor *
    # change course data like image/name/period/max or min students.... *
    # if admin1 *
        # register admins 
        # delete admins
        # change admins info
    return render_template('admins/new_control_panel.html', value=request.args.get("value"))



@admins_blueprint.route("/admins/register", methods=["GET", "POST"])
@login_required(["admin1"])
def register(): # create an email and add email verification functionality

    form = AdminRegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        admin_type = form.admin_type.data
        
        email_confirmation_code = generate_random_digits(5)

        user = UserModel(username=username, first_name=first_name, last_name=last_name, email=email, password=password,
        email_confirmation_code=email_confirmation_code, user_type=admin_type)

        db.session.add(user)
        db.session.commit()
        admin_date_model = AdminDataModel(user=user)
        db.session.add(admin_date_model)
        db.session.commit()


        send_user_confirmation_email(email, email_confirmation_code)

        return redirect(url_for("users_blueprint.email_confirmation"))
    return render_template('admins/register.html', form=form)  



# @admins_blueprint.route("/admins/courses", methods=["GET"])
# @login_required(ADMIN_TYPES)
# def courses():
#     return render_template("admins/courses.html")

@admins_blueprint.route("/admins/courses/create-course", methods=["GET", "POST"])
@login_required(ADMIN_TYPES)
def add_course():
    form = AdminCourseCreationForm()
    tutors = UserModel.query.filter_by(user_type="tutor").all()
    tutors = [tutor for tutor in tutors if tutor.tutor_data_model.is_accepted == True]
    tutors_select_tuple = list_to_select_compatable_tuple(tutors, "id", "full_name")
    form.tutors.choices = tutors_select_tuple
    form.subject.choices = json_list_to_select_compatable_tuple(SiteSettingsModel.instance().subjects["setting_value"])

    if form.validate_on_submit():
        course_name = form.name.data
        course_description = form.description.data
        course_type = int(form.course_type.data)
        price = form.price.data
        subject = form.subject.data
        period = int(form.period.data) if form.period.data else None
        currency = form.currency.data
        min_students = form.min_students.data
        max_students = form.max_students.data if course_type == 2 else min_students
        start_date = form.start_date.data
        end_date = form.end_date.data 
        links = json.dumps({"students_zoom_link" : form.students_zoom_link.data, "tutor_zoom_link": form.tutor_zoom_link.data})
        table = {
            "sunday": {"from": str(form.sunday_start.data), "to": str(form.sunday_end.data)},
            "monday": {"from": str(form.monday_start.data), "to": str(form.monday_end.data)},
            "tuesday": {"from": str(form.tuesday_start.data), "to": str(form.tuesday_end.data)},
            "wednesday": {"from": str(form.wednesday_start.data), "to": str(form.wednesday_end.data)},
            "thursday": {"from": str(form.thursday_start.data), "to": str(form.thursday_end.data)},
            "friday": {"from": str(form.friday_start.data), "to": str(form.friday_end.data)},
            "saturday": {"from": str(form.saturday_start.data), "to": str(form.saturday_end.data)}
        }
        weekly_time_table_json = json.dumps(table)
       
        tutor_data_model = UserModel.query.get(int(form.tutors.data)).tutor_data_model
        if subject not in tutor_data_model.subjects:
            flash("المادة المختارة في الكورس ليست من ضمن المواد التي يدرسها المعلم المختار", "danger")
            return redirect(url_for("admins_blueprint.add_course"))
        elif not tutor_data_model.is_accepted:
            flash("هذاالمعلم لم يقبل بعد", "danger")
            return redirect(url_for("admins_blueprint.add_course"))
        course = CourseModel(name=course_name, description=course_description, created_by_admin=True,
         tutor=tutor_data_model, price=price, min_students=min_students, max_students=max_students, currency=currency, 
         _period=period, course_type=course_type, subject=subject, _start_date=start_date, _end_date=end_date, 
         weekly_time_table_json=weekly_time_table_json, links=links)
        db.session.add(course)
        payment_model = PaymentModel(course=course)
        db.session.add(payment_model)
        db.session.commit()
        return redirect(url_for("courses_blueprint.courses"))
    return render_template("admins/new_create_course.html", form=form)


@admins_blueprint.route("/admins/all_users", methods=["GET"])
@login_required(ADMIN_TYPES)
def users_list_view(): # admin only
    users = UserModel.query.all()
    return render_template("admins/users.html", users=users)

@admins_blueprint.route("/admins/user/<user_id>", methods=["GET"])
@login_required(ADMIN_TYPES)
def user_detailed_view(user_id): # admin only
    user = UserModel.query.get(user_id)
    user_type = user.user_type
    if user_type == "tutor":
        return render_template("admins/users/new_tutor.html", user=user)
    elif user_type == "student":
        return render_template("admins/users/new_student.html", user=user)
    elif user_type in ADMIN_TYPES:
        return render_template("admins/users/new_admin.html", user=user)


@admins_blueprint.route("/admins/change-site-settings")
@login_required(ADMIN_TYPES)
def change_site_settings(): # there should be a 
    setting_name = str(request.args.get("setting"))
    
    settings = SiteSettingsModel.instance()
    setting = getattr(settings, setting_name)
    setting_type = setting["setting_type"]
    value = None
    if setting_type == bool.__name__:
        settings.reverse_bool_setting(setting_name)
    elif setting_type == list.__name__: # what if i wanted to remove?
        value = str(request.args.get("value"))
        change_action_name = str(request.args.get("change_action_name"))
        if change_action_name == "add":
            settings.add_to_list_type_setting(setting_name, value)
        elif change_action_name == "remove":
            settings.remove_from_list_type_setting(setting_name, value)
    elif setting_type == dict.__name__: # also what if i wanted to remove?
        key = str(request.args.get("key"))
        value = str(request.args.get("value"))
        settings.add_or_change_to_dict_type_setting(setting_name, key, value)

    return redirect(url_for("admins_blueprint.control_panel", vlaue=value))


@admins_blueprint.route("/admins/accept-tutor/<tutor_id>", methods=["GET"])
@login_required(ADMIN_TYPES)
def accept_tutor(tutor_id): # admin only
    tutor = TutorDataModel.query.get(tutor_id)
    tutor.is_accepted = True 
    db.session.commit()
    send_tutor_accepted_email(tutor)
    return redirect(url_for('admins_blueprint.user_detailed_view', user_id=tutor.user.id))

@admins_blueprint.route("/admins/leave-requests", methods=["GET"])
@login_required(ADMIN_TYPES)
def requests_list(): # admin only
    storage = AdminstrationStorageModel.instance()
    new_leave_requests = {}
    if storage.has_leave_requests():
        leave_requests = storage.leave_requests
        for student_id in leave_requests: #'{"student_id": [{"course_id": ..., "date": ..., "status": "pending"/"accepted"/"denied"}, {}], ....}'
            new_leave_requests[StudentDataModel.query.get(int(student_id))] = leave_requests[student_id] # change key to student pointer
            # change courses id's to courses pointers
            for student in new_leave_requests:
                for i, request in enumerate(new_leave_requests[student]):
                    new_leave_requests[student][i] = {"course": CourseModel.query.get(new_leave_requests[student][i].get("course_id")), "date": new_leave_requests[student][i].get("date"), "status": new_leave_requests[student][i].get("status")} 
    return render_template("admins/leave_requests.html", requests=new_leave_requests)


@admins_blueprint.route("/admins/reply-leave-request/<reply>/<student_id>/<course_id>", methods=["GET"])
@login_required(ADMIN_TYPES)
def reply_to_leave_request(reply, student_id, course_id): # admin only
    storage = AdminstrationStorageModel.instance()
    if reply == "accept":
        storage.accept_leave_request(student_id, course_id)
    elif reply == "deny":
        storage.deny_leave_request(student_id, course_id)
    return redirect(url_for('admins_blueprint.requests_list'))

# @admins_blueprint.route("/admins/profile", methods=["GET"])
# @login_required([i for i in ADMIN_TYPES])
# def profile():
#     return render_template("admins/admin_profile.html")


# @users_blueprint.route("/users/profile/edit", methods=["GET", "POST"])
# @login_required([])
# def edit_profile():
#     form = EditProfileForm()

#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user.first_name = form.first_name.data
#         current_user.last_name = form.last_name.data
#         current_user.date_of_birth = form.date_of_birth.data
#         current_user.school_name = form.school_name.data

#         db.session.commit()

#         # on email change
#         if form.email.data != current_user.email:
#             new_email = form.email.data
#             serialized_id_and_email = current_user.get_email_change_token(new_email=new_email)
#             send_email_change_request_email(new_email, serialized_id_and_email)

#         return redirect(url_for("users_blueprint.profile"))

#     elif request.method == "GET":
#         form.username.data = current_user.username
#         form.first_name.data = current_user.first_name
#         form.last_name.data = current_user.last_name
#         form.email.data = current_user.email
#         form.date_of_birth.data = current_user.date_of_birth
#         form.school_name.data = current_user.school_name

#     return render_template('users/edit_profile.html', form=form)  





# @users_blueprint.route("/users/all_users", methods=["GET", "POST"])
# @login_required([])
# def users_list_view(): # admin only
#     users = UserModel.query.all()
#     profiles_images_path = url_for("static", filename="profiles/images")
#     return render_template("users/all_users.html", users=users, profile_images_path=profiles_images_path)

# @users_blueprint.route("/users/<user_id>", methods=["GET", "POST"])
# @login_required([])
# def user_detailed_view(user_id): #admin only
#     user = UserModel.query.get(int(user_id))
#     if user == current_user:
#         return redirect(url_for("users_blueprint.profile"))
        
#     profiles_images_path = url_for("static", filename="profiles/images")
#     user_profile_image = os.path.join(profiles_images_path, user.profile_image_name)

#     followers = [UserModel.query.get(follower.follower_user_id) for follower in current_user.followers]
#     following = [UserModel.query.get(following.followed_user_id) for following in current_user.following]
#     return render_template("users/user.html", user=user, profile_image=user_profile_image, followers=followers, followings=following)





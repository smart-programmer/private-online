from flask import Blueprint, render_template, request, redirect, url_for, make_response, flash, current_app
from flask_login import current_user, login_user, logout_user
from TUTOR import db, bcrypt
from TUTOR.STUDENTS.forms import StudentRegistrationForm, StudentEditProfileForm
from TUTOR.models import UserModel, StudentDataModel, CourseModel, SiteSettingsModel
from TUTOR.utils.mail import send_user_confirmation_email, send_student_course_join_email, send_student_leave_course_email, send_student_pay_for_course_email, send_tutor_course_start_email
from TUTOR.utils.utils import generate_random_digits, login_required, put_current_choice_first
from TUTOR.utils.languages import LngObj
from TUTOR.settings import LANGUAGES, ADMIN_TYPES


students_blueprint = Blueprint("students_blueprint", __name__)


@students_blueprint.context_processor
def utility_processor():
    return dict(get_language_text=LngObj.get_language_text, get_current_page_language_list=LngObj.get_current_page_language_list, languages=LANGUAGES, admin_types=ADMIN_TYPES, settings=SiteSettingsModel.instance())


@students_blueprint.route('/students')
@login_required(["student"])
def home():
    return render_template("students/index.html")


@students_blueprint.route("/students/register", methods=["GET", "POST"])
def register(): # create an email and add email verification functionality
    if current_user.is_authenticated:
        return redirect("main_blueprint.home")

    form = StudentRegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        gender = bool(int(form.gender.data))
        date_of_birth = form.date_of_birth.data
        password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user_type = "student"
        
        email_confirmation_code = generate_random_digits(5)

        user = UserModel(username=username, first_name=first_name, last_name=last_name, email=email, password=password,
        email_confirmation_code=email_confirmation_code, user_type=user_type, _gender=gender)


        db.session.add(user)
        db.session.commit()
        student_data_model = StudentDataModel(user=user, date_of_birth=date_of_birth)
        db.session.add(student_data_model)
        db.session.commit()

        send_user_confirmation_email(email, email_confirmation_code)

        return redirect(url_for("users_blueprint.email_confirmation"))

    return render_template('students/student_register.html', form=form)  


@students_blueprint.route("/students/profile", methods=["GET", "POST"])
@login_required(["student"])
def profile():
    return render_template("students/student_profile.html")


@students_blueprint.route("/students/profile/edit", methods=["GET", "POST"])
@login_required(["student"])
def edit_profile():
    student_data_model = current_user.student_data_model

    form = StudentEditProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        student_data_model.date_of_birth = form.date_of_birth.data
        current_user._gender = bool(int(form.gender.data))
        

        db.session.commit()

        # on email change
        if form.email.data != current_user.email:
            new_email = form.email.data
            serialized_id_and_email = current_user.get_email_change_token(new_email=new_email)
            send_email_change_request_email(new_email, serialized_id_and_email)

        return redirect(url_for("students_blueprint.profile"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.date_of_birth.data = student_data_model.date_of_birth
        form.gender.choices = put_current_choice_first(form.gender.choices, str(int(current_user._gender)))

    return render_template('students/edit_student_profile.html', form=form, gender_choices=form.gender.choices)  


@students_blueprint.route("/students/courses/my-courses", methods=["GET"])
@login_required(["student"])
def my_courses():
    courses = current_user.student_data_model.courses
    return render_template('students/my_courses.html', courses=courses)


@students_blueprint.route("/students/courses/join-course/<course_id>", methods=["GET"])
@login_required(["student"])
def join_course(course_id):
    # if course has began or has ended or has reached max user or was canceled then don't allow for new students
    # in other words: test course state then choose what to do
    # so i need to make a new course state system for example {"state_coude": 1, "state_string": "pending"}
    student_data_model = current_user.student_data_model
    course = CourseModel.query.get(course_id)
    if course.can_join(student_data_model): 
        course.add_student(student_data_model)
        send_student_pay_for_course_email(student_data_model.user, course)

    # if course.should_send_first_payment_emails():
    #     course.send_all_payment_emails()

    return redirect(url_for("courses_blueprint.course", course_id=course_id))

@students_blueprint.route("/students/courses/leave-course/<course_id>", methods=["GET"])
@login_required(["student"])
def leave_course(course_id): # cannot leave after payment but a leave request is put to be revised by admins and if admin agrees payment is refunded
    student_data_model = current_user.student_data_model
    course = CourseModel.query.get(course_id)
    #if student.has_paid:
        # put leave request to admins 
        # return redirect(url_for("students_blueprint.my_courses")) 
    # else:
    student_data_model.courses.remove(course)
    db.session.commit()
    send_student_leave_course_email(current_user, course)
    #send email with
    return redirect(url_for("students_blueprint.my_courses"))



    



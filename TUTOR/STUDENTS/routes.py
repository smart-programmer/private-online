from flask import Blueprint, render_template, request, redirect, url_for, make_response, flash, current_app
from flask_login import current_user, login_user, logout_user
from TUTOR import db, bcrypt
from TUTOR.STUDENTS.forms import StudentRegistrationForm, StudentEditProfileForm
from TUTOR.USERS.models import UserModel
from TUTOR.STUDENTS.models import StudentDataModel
from TUTOR.utils.mail import send_user_confirmation_email
from TUTOR.utils.utils import generate_random_digits, login_required
from TUTOR.utils.languages import LngObj
from TUTOR.settings import LANGUAGES


students_blueprint = Blueprint("students_blueprint", __name__)


@students_blueprint.context_processor
def utility_processor():
    return dict(get_language_text=LngObj.get_language_text, get_current_page_language_list=LngObj.get_current_page_language_list, languages=LANGUAGES)


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
        school_name = form.school_name.data
        date_of_birth = form.date_of_birth.data
        password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user_type = "student"
        
        email_confirmation_code = generate_random_digits(5)

        user = UserModel(username=username, first_name=first_name, last_name=last_name, email=email, password=password,
        email_confirmation_code=email_confirmation_code, user_type=user_type)


        db.session.add(user)
        db.session.commit()
        student_data_model = StudentDataModel(user_id=user.id, school_name=school_name, date_of_birth=date_of_birth)
        db.session.add(student_data_model)
        db.session.commit()

        send_user_confirmation_email(email, email_confirmation_code)

        return redirect(url_for("users_blueprint.email_confirmation"))
    return render_template('students/student_register.html', form=form)  


@students_blueprint.route("/students/profile", methods=["GET", "POST"])
@login_required(["student"])
def profile():
    student_data_model = StudentDataModel.query.get(current_user.id)
    return render_template("students/student_profile.html", student_data_model=student_data_model)


@students_blueprint.route("/students/profile/edit", methods=["GET", "POST"])
@login_required(["student"])
def edit_profile():
    student_data_model = StudentDataModel.query.get(current_user.id)

    form = StudentEditProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        student_data_model.school_name = form.school_name.data
        student_data_model.date_of_birth = form.date_of_birth.data
        

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
        form.school_name.data = student_data_model.school_name
        form.date_of_birth.data = student_data_model.date_of_birth

    return render_template('students/edit_student_profile.html', form=form)  










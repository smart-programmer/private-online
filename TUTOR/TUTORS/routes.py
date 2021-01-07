from flask import Blueprint, render_template, request, redirect, url_for, make_response, flash, current_app
from flask_login import current_user, login_user, logout_user
from TUTOR import db, bcrypt
from TUTOR.TUTORS.forms import TutorRegistrationForm, TutorEditProfileForm, CourseCreationForm
from TUTOR.models import UserModel, TutorDataModel, CourseModel, SiteSettingsModel
from TUTOR.utils.mail import send_user_confirmation_email
from TUTOR.utils.utils import generate_random_digits, login_required
from TUTOR.utils.languages import LngObj
from TUTOR.settings import LANGUAGES, ADMIN_TYPES


tutors_blueprint = Blueprint("tutors_blueprint", __name__)


@tutors_blueprint.context_processor
def utility_processor():
    return dict(get_language_text=LngObj.get_language_text, get_current_page_language_list=LngObj.get_current_page_language_list, languages=LANGUAGES, admin_types=ADMIN_TYPES, settings=SiteSettingsModel.get_settings_dict())


@tutors_blueprint.route('/tutors')
@login_required(["tutor"])
def home():
    return render_template("tutors/index.html")


@tutors_blueprint.route("/tutors/register", methods=["GET", "POST"])
def register(): # create an email and add email verification functionality
    if current_user.is_authenticated:
        return redirect("main_blueprint.home")


    form = TutorRegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        gender = bool(int(form.gender.data))
        date_of_birth = form.date_of_birth.data
        nationality = form.nationality.data
        qualification = form.qualification.data
        major = form.major.data
        current_job = form.current_job.data
        subjects = form.subjects.data
        years_of_experience = form.years_of_experience.data
        tools_used_for_online_tutoring = form.tools_used_for_online_tutoring.data
        password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user_type = "tutor"
        
        email_confirmation_code = generate_random_digits(5)

        user = UserModel(username=username, first_name=first_name, last_name=last_name, email=email, password=password,
        email_confirmation_code=email_confirmation_code, user_type=user_type, _gender=gender)


        db.session.add(user)
        db.session.commit()
        tutor_data_model = TutorDataModel(user=user, date_of_birth=date_of_birth, nationality=nationality, qualification=qualification, major=major,
        current_job=current_job, _subjects=subjects, years_of_experience=years_of_experience,
        _tools_used_for_online_tutoring=tools_used_for_online_tutoring)
        db.session.add(tutor_data_model)
        db.session.commit()

        send_user_confirmation_email(email, email_confirmation_code)

        return redirect(url_for("users_blueprint.email_confirmation"))
    return render_template('tutors/tutor_register.html', form=form)  


@tutors_blueprint.route("/tutors/profile", methods=["GET", "POST"])
@login_required(["tutor"])
def profile():
    return render_template("tutors/tutor_profile.html")


@tutors_blueprint.route("/tutors/profile/edit", methods=["GET", "POST"])
@login_required(["tutor"])
def edit_profile():
    tutor_data_model = current_user.tutor_data_model

    form = TutorEditProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user._gender = bool(int(form.gender.data))
        current_user.tutor_data_model.date_of_birth = form.date_of_birth.data
        current_user.tutor_data_model.nationality = form.nationality.data
        current_user.tutor_data_model.qualification = form.qualification.data
        current_user.tutor_data_model.major = form.major.data
        current_user.tutor_data_model.current_job = form.current_job.data
        if form.subjects.data.strip():
            current_user.tutor_data_model._subjects =  TutorDataModel.list_to_comma_seperated_string(current_user.tutor_data_model.subjects + form.subjects.data.split(","))
        current_user.tutor_data_model.years_of_experience = form.years_of_experience.data
        if form.tools_used_for_online_tutoring.data.strip():
            current_user.tutor_data_model._tools_used_for_online_tutoring = TutorDataModel.list_to_comma_seperated_string(current_user.tutor_data_model.tools_used_for_online_tutoring + form.tools_used_for_online_tutoring.data.split(","))

        db.session.commit()

        # on email change
        if form.email.data != current_user.email:
            new_email = form.email.data
            serialized_id_and_email = current_user.get_email_change_token(new_email=new_email)
            send_email_change_request_email(new_email, serialized_id_and_email)

        return redirect(url_for("tutors_blueprint.profile"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.date_of_birth.data = current_user.tutor_data_model.date_of_birth
        form.nationality.data = current_user.tutor_data_model.nationality
        form.major.data = current_user.tutor_data_model.major
        form.qualification.data = current_user.tutor_data_model.qualification
        form.current_job.data = current_user.tutor_data_model.current_job
        form.years_of_experience.data = current_user.tutor_data_model.years_of_experience
        form.gender.data = current_user.gender

    return render_template('tutors/edit_tutor_profile.html', form=form)  





@tutors_blueprint.route("/tutors/create-course", methods=["GET", "POST"])
@login_required(["tutor"])
def add_course():
    if current_user.user_type == "tutor":
        if not SiteSettingsModel.get_settings_dict()["allow_tutors_to_create_courses"]:
            return current_app.login_manager.unauthorized()    
    form = CourseCreationForm()
    

    if form.validate_on_submit():
        course_name = form.name.data
        course_description = form.description.data
        price = form.price.data
        currency = form.currency.data
        min_students = form.min_students.data
        max_students = form.max_students.data
        course = CourseModel(name=course_name, description=course_description, created_by_admin=False,
         tutor=current_user.tutor_data_model, price=price, min_students=min_students, max_students=max_students, currency=currency)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for("courses_blueprint.courses"))
    return render_template("tutors/create_course.html", form=form)

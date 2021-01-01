from flask import Blueprint, render_template, request, redirect, url_for, make_response, flash, current_app
from flask_login import current_user, login_user, logout_user
from TUTOR import db, bcrypt
from TUTOR.ADMINISTRATION.forms import AdminRegistrationForm
from TUTOR.USERS.models import UserModel
from TUTOR.ADMINISTRATION.models import AdminDataModel
from TUTOR.utils.mail import send_user_confirmation_email, send_user_reset_password_email, send_user_change_password_email, send_email_change_request_email, send_deny_email_change_email
from TUTOR.utils.utils import save_image_locally, delete_image, generate_random_digits, login_required
from TUTOR.settings import ADMIN_TYPES, LANGUAGES
from TUTOR.utils.languages import LngObj
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os


admins_blueprint = Blueprint("admins_blueprint", __name__)

@admins_blueprint.context_processor
def utility_processor():
    return dict(get_language_text=LngObj.get_language_text, get_current_page_language_list=LngObj.get_current_page_language_list, languages=LANGUAGES)


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
    return render_template('admins/control_panel.html', admin_types=ADMIN_TYPES)



@admins_blueprint.route("/admins/register", methods=["GET", "POST"])
@login_required(["admin1"])
def register(): # create an email and add email verification functionality

    form = RegistrationForm()
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



@admins_blueprint.route("/admins/courses", methods=["GET"])
@login_required(ADMIN_TYPES)
def courses():
    return render_template("admins/admin_courses.html")


@admins_blueprint.route("/users/all_users", methods=["GET", "POST"])
@login_required(ADMIN_TYPES)
def users_list_view(): # admin only
    users = UserModel.query.all()
    return render_template("admins/users.html", users=users)


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





from flask import Blueprint, render_template, request, redirect, url_for, make_response, flash, current_app
from flask_login import current_user, login_user, login_required, logout_user
from SPORT import db, bcrypt
from SPORT.USERS.forms import RegistrationForm, LoginForm, EditProfileForm, ConfirmationCodeForm, RequestResetPasswordForm, ResetPasswordForm, ChangePasswordForm
from SPORT.USERS.models import UserModel
from SPORT.utils.mail import send_user_confirmation_email, send_user_reset_password_email, send_user_change_password_email, send_email_change_request_email, send_deny_email_change_email
from SPORT.utils.utils import  save_image_locally, delete_image, generate_random_digits
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os


users_blueprint = Blueprint("users_blueprint", __name__)


@users_blueprint.route("/users/register", methods=["GET", "POST"])
def register(): # create an email and add email verification functionality
    if current_user.is_authenticated:
        return redirect("main_blueprint.home")

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        age = form.age.data
        biography = form.biography.data
        if form.profile_image.data:
            image_name, image_path = save_image_locally(form.profile_image.data, "static/profiles/images")
        
        email_confirmation_code = generate_random_digits(5)

        user = UserModel(username=username, first_name=first_name, last_name=last_name, email=email, password=password,
        age=age, biography=biography, profile_image_name=image_name, email_confirmation_code=email_confirmation_code) if form.profile_image.data else UserModel(username=username, first_name=first_name, last_name=last_name, email=email, password=password,
        age=age, biography=biography, email_confirmation_code=email_confirmation_code)

        db.session.add(user)
        db.session.commit()

        send_user_confirmation_email(email, email_confirmation_code)

        return redirect(url_for("users_blueprint.email_confirmation"))
    return render_template('users/register.html', form=form)  

@users_blueprint.route("/users/confirm_email", methods=["GET", "POST"])
def email_confirmation():
    if current_user.is_authenticated:
        logout_user()
        
    form = ConfirmationCodeForm()
    if form.validate_on_submit():
        code = form.code.data
        user = UserModel.query.filter_by(email_confirmation_code=code).first()
        if user:
            user.is_confirmed = True
            user.email_confirmation_code = None
            db.session.commit()
            return redirect(url_for("users_blueprint.login"))
        else:
            return redirect(url_for("users_blueprint.email_confirmation"))
    return render_template("users/email_verification.html", form=form)


@users_blueprint.route("/users/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main_blueprint.home"))
    
    redirected = request.args.get("redirected")
    if redirected == "wrong":
        flash("wrong credentials, please try again.", "error")

    form = LoginForm()

    if form.validate_on_submit():
        username_or_email = form.username_or_email.data
        user = UserModel.query.filter_by(email=username_or_email).first()
        user = user if user else UserModel.query.filter_by(username=username_or_email).first() 
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                if user.is_confirmed:
                    login_user(user, remember=True)
                    next_page = request.args.get("next")
                    return redirect(next_page) if next_page else redirect(url_for("users_blueprint.profile"))
                else:
                    return redirect(url_for("users_blueprint.login", redirected="not_confirmed"))
            else:
                return redirect(url_for("users_blueprint.login", redirected="wrong"))
        else:
            return redirect(url_for("users_blueprint.login", redirected="wrong"))
    return render_template('users/login.html', form=form)

@users_blueprint.route("/users/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main_blueprint.home"))

@users_blueprint.route("/users/request_reset_password", methods=["GET", "POST"])
def request_reset_password():
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        username_or_email = form.username_or_email.data
        user = UserModel.query.filter_by(email=username_or_email).first()
        user = user if user else UserModel.query.filter_by(username=username_or_email).first() 
        send_user_reset_password_email(user.email, user.get_reset_token())
        return redirect(url_for("users_blueprint.login"))
    return render_template("users/request_reset_password.html", form=form)

@users_blueprint.route("/users/reset_password/<user_serialized_id>", methods=["GET", "POST"])
def reset_password(user_serialized_id):
    user = UserModel.verify_reset_token(user_serialized_id)
    form = ResetPasswordForm()
    if user:
        if form.validate_on_submit():
            password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user.password = password
            db.session.commit()
            return redirect(url_for("users_blueprint.login"))
    else:
        flash("reset token time expired, try again", "error")
        return redirect(url_for("users_blueprint.request_reset_password"))
    return render_template("users/reset_password.html", form=form)

@users_blueprint.route("/users/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            new_password = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
            current_user.password = new_password
            db.session.commit()
            send_user_change_password_email(current_user.email, current_user.get_reset_token())
            flash("changing password, please wait", "info")
            return redirect(url_for("users_blueprint.profile"))
    return render_template("users/change_password.html", form=form)

@users_blueprint.route("/users/change_email/<user_serialized_id_and_email>", methods=["GET", "POST"])
@login_required
def change_email(user_serialized_id_and_email):
    user, new_email = UserModel.verify_email_change_token(user_serialized_id_and_email)
    old_email = user.email
    user.email = new_email
    db.session.commit()
    logout_user()

    # send email revert to original email in case of account theft situation
    s = Serializer(current_app.config.get("SECRET_KEY"), 1800) 
    token = s.dumps({"old_email": old_email, "user_id": user.id})
    send_deny_email_change_email(old_email, token)

    return redirect(url_for("users_blueprint.login"))

@users_blueprint.route("/users/revert_email_change/<user_serialized_id_and_email>", methods=["GET", "POST"])
def deny_email_change(user_serialized_id_and_email):
    s = Serializer(current_app.config.get("SECRET_KEY")) 
    try:
        user_id = s.loads(user_serialized_id_and_email)["user_id"]
    except:
        return redirect("main_blueprint.home")
    try:
        old_email = s.loads(user_serialized_id_and_email)["old_email"]
    except:
        return redirect("main_blueprint.home")
    
    user = UserModel.query.get(user_id)
    user.email = old_email
    db.session.commit()
    logout_user()
    return redirect(url_for("users_blueprint.login"))

@users_blueprint.route("/users/profile")
@login_required
def profile():
    profiles_images_path = url_for("static", filename="profiles/images")
    user_profile_image = os.path.join(profiles_images_path, current_user.profile_image_name)
    return render_template("users/user_profile.html", path=profiles_images_path, profile_image=user_profile_image)


@users_blueprint.route("/users/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    profiles_images_path = url_for("static", filename="profiles/images")
    user_profile_image = os.path.join(profiles_images_path, current_user.profile_image_name)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.age = form.age.data
        current_user.biography = form.biography.data
        if form.profile_image.data:
            if current_user.profile_image_name != "default.png":
                delete_image(user_profile_image)
            image_name, image_path = save_image_locally(form.profile_image.data, "static/profiles/images")
            current_user.profile_image_name = image_name

        db.session.commit()

        # on email change
        if form.email.data != current_user.email:
            new_email = form.email.data
            serialized_id_and_email = current_user.get_email_change_token(new_email=new_email)
            send_email_change_request_email(new_email, serialized_id_and_email)

        return redirect(url_for("users_blueprint.profile"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.age.data = current_user.age
        form.biography.data = current_user.biography

    return render_template('users/edit_profile.html', form=form, profile_image=user_profile_image)  





@users_blueprint.route("/users/all_users", methods=["GET", "POST"])
@login_required
def users_list_view():
    users = UserModel.query.all()
    profiles_images_path = url_for("static", filename="profiles/images")
    return render_template("users/all_users.html", users=users, profile_images_path=profiles_images_path)

@users_blueprint.route("/users/<user_id>", methods=["GET", "POST"])
@login_required
def user_detailed_view(user_id):
    user = UserModel.query.get(int(user_id))
    profiles_images_path = url_for("static", filename="profiles/images")
    user_profile_image = os.path.join(profiles_images_path, user.profile_image_name)
    return render_template("users/user.html", user=user, profile_image=user_profile_image)



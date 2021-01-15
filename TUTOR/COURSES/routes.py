from flask import Blueprint, render_template, make_response, current_app, request, url_for, redirect
from flask_login import current_user
from TUTOR import db
from TUTOR.utils.utils import reverse_url_for, parse_view_name, login_required
from TUTOR.utils.languages import LngObj
from TUTOR.settings import LANGUAGES, ADMIN_TYPES
from TUTOR.models import CourseModel, SiteSettingsModel
from TUTOR.COURSES.forms import CourseCreationForm


# a blueprint for unauthorised users or views for all types of users

courses_blueprint = Blueprint("courses_blueprint", __name__)

@courses_blueprint.context_processor
def utility_processor():
    return dict(get_language_text=LngObj.get_language_text, get_current_page_language_list=LngObj.get_current_page_language_list, languages=LANGUAGES, admin_types=ADMIN_TYPES, settings=SiteSettingsModel.get_settings_dict())


@courses_blueprint.route("/courses")
@login_required([])
def courses():
    all_courses = CourseModel.query.all()
    return render_template("courses.html", all_courses=all_courses)

@courses_blueprint.route("/courses/<course_id>")
@login_required([])
def course(course_id):
    course = CourseModel.query.get(course_id)
    return render_template("course.html", course=course)

@courses_blueprint.route("/courses/control-course/<course_id>")
@login_required(ADMIN_TYPES + ["tutor"]) # check if admin allowes tutors to edit
def control_course(course_id):
    if current_user.user_type == "tutor":
        if not SiteSettingsModel.get_str_bool(SiteSettingsModel.query.filter_by(name="allow_tutors_to_edit_courses").first().value):
            return current_app.login_manager.unauthorized()    
    # here one can edit course data or delete course or begin or end it
    course = CourseModel.query.get(course_id)
    # if user.user_type is tutor make a can edit variable
    return render_template("control_course.html", course=course)




@courses_blueprint.route("/courses/control-course/<course_id>/end")
@login_required(ADMIN_TYPES + ["tutor"]) # check if admin allowes tutors to edit
def end_course(course_id):
    if current_user.user_type == "tutor":
        if not SiteSettingsModel.get_str_bool(SiteSettingsModel.query.filter_by(name="allow_tutors_to_edit_courses").first().value):
            return current_app.login_manager.unauthorized()    
    # check if course has already ended or if it hasen't started
    course = CourseModel.query.get(course_id)
    course.ended = True
    db.session.commit()
    return render_template("control_course.html", course=course)










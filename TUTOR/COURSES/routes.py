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
    return dict(get_language_text=LngObj.get_language_text, get_current_page_language_list=LngObj.get_current_page_language_list, languages=LANGUAGES, admin_types=ADMIN_TYPES, settings=SiteSettingsModel.instance())


@courses_blueprint.route("/courses")
@login_required([])
def courses():
    all_courses = CourseModel.query.all()
    return render_template("courses.html", all_courses=all_courses)

@courses_blueprint.route("/courses/<course_id>")
@login_required([])
def course(course_id):
    course = CourseModel.query.get(course_id)
    is_allowed = CourseModel.is_allowed_to_control_course(course, current_user)
    user_type = current_user.user_type
    if user_type == "student":
        return render_template("students/course.html", course=course, is_allowed=is_allowed)
    elif user_type == "tutor":
        return render_template("tutors/course.html", course=course, is_allowed=is_allowed)
    elif user_type in ADMIN_TYPES:
        return render_template("admins/course.html", course=course, is_allowed=is_allowed)


# the views below are commented because we decided that everything will be automated instead of 
# someone starting and ending the courses

# @courses_blueprint.route("/courses/control-course/<course_id>")
# @login_required(ADMIN_TYPES + ["tutor"]) # check if admin allowes tutors to edit
# def control_course(course_id):
#     # if current_user.user_type == "tutor":
#     #     if not SiteSettingsModel.get_str_bool(SiteSettingsModel.query.filter_by(name="allow_tutors_to_edit_courses").first().value):
#     course = CourseModel.query.get(course_id)
#     if not course or not CourseModel.is_allowed_to_control_course(course, current_user):
#         return current_app.login_manager.unauthorized()    
#     # here one can edit course data or delete course or begin or end it
#     # if user.user_type is tutor make a can edit variable
#     return render_template("control_course.html", course=course)



# @courses_blueprint.route("/courses/control-course/<course_id>/end")
# @login_required(ADMIN_TYPES + ["tutor"]) # check if admin allowes tutors to edit
# def start_course(course_id):
#     if CourseModel.is_allowed_to_control_course(current_user):
#         return True
#     course = CourseModel.query.get(course_id)
#     if not course or not CourseModel.is_allowed_to_control_course(course, current_user):
#         return current_app.login_manager.unauthorized()    
#     course.began = True
#     db.session.commit()
#     # send emails
#     return redirect(url_for("course", course_id=course_id))




# @courses_blueprint.route("/courses/control-course/<course_id>/end")
# @login_required(ADMIN_TYPES + ["tutor"]) # check if admin allowes tutors to edit
# def end_course(course_id):
#     course = CourseModel.query.get(course_id)
#     if not course or not CourseModel.is_allowed_to_control_course(course, current_user):
#         return current_app.login_manager.unauthorized()        
#     # check if course has already ended or if it hasen't started
#     course.ended = True
#     db.session.commit()
#     return redirect(url_for("course", course_id=course_id))










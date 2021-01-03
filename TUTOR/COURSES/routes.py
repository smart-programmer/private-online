from flask import Blueprint, render_template, make_response, current_app, request, url_for, redirect
from flask_login import current_user
from TUTOR.utils.utils import reverse_url_for, parse_view_name, login_required
from TUTOR.utils.languages import LngObj
from TUTOR.settings import LANGUAGES, ADMIN_TYPES
from TUTOR.models import CourseModel
from TUTOR.COURSES.forms import CourseCreationForm


# a blueprint for unauthorised users or views for all types of users

courses_blueprint = Blueprint("courses_blueprint", __name__)

@courses_blueprint.context_processor
def utility_processor():
    return dict(get_language_text=LngObj.get_language_text, get_current_page_language_list=LngObj.get_current_page_language_list, languages=LANGUAGES)


@courses_blueprint.route("/courses")
def courses():
    courses = CourseModel.query.all()
    return render_template("courses.html", courses=courses)

@courses_blueprint.route("/courses/<course_id>")
def course(course_id):
    course = CourseModel.query.get(course_id)
    return render_template("course.html", course=course)


@courses_blueprint.route("/courses/create-course")
@login_required(["tutor"])
def add_course():
    form = CourseCreationForm()

    if form.validate_on_submit():
        course_name = form.name.data
        course_description = form.description.data
        course = CourseModel(name=course_name, descricption=course_description, created_by_admin=False)
        db.session.add(courses)
        db.session.commit()
        return redirect(url_for("courses_blueprint.courses"))
    return render_template("course.html", course=course)










from flask import Blueprint, render_template, make_response, current_app, request, url_for, redirect
from flask_login import current_user
from TUTOR.utils.utils import reverse_url_for, parse_view_name, login_required
from TUTOR.utils.languages import LngObj
from TUTOR.settings import LANGUAGES, ADMIN_TYPES
from TUTOR.models import CourseModel
from TUTOR.COURSES.forms import PaymentForm



payment_blueprint = Blueprint("payment_blueprint", __name__)

@payment_blueprint.context_processor
def utility_processor():
    return dict(get_language_text=LngObj.get_language_text, get_current_page_language_list=LngObj.get_current_page_language_list, languages=LANGUAGES, admin_types=ADMIN_TYPES)


@payment_blueprint.route("/pay/<course_id>", methods=["GET", "POST"])
@login_required('student')
def student_course_pay(course_id):
    course = CourseModel.query.get(int(course_id))
    payment_model = course.payment_model
    student = current_user.student_data_model
    if course.can_join(student):
        payment_model.pay()
    return render_template("courses.html", all_courses=all_courses)

# @payment_blueprint.route("/pay")
# @login_required('student')
# def student_course_pay(course_id):
#     course = CourseModel.query.get(int(course_id))

#     return render_template("courses.html", all_courses=all_courses)

# @payment_blueprint.route("/courses/<course_id>")
# def course(course_id):
#     course = CourseModel.query.get(course_id)
#     return render_template("course.html", course=course)












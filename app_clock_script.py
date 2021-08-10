from apscheduler.schedulers.blocking import BlockingScheduler
from TUTOR import create_app
from TUTOR.config import Production_Config
from TUTOR.models import CourseModel
import os

production = os.environ.get("production")
app = None
if not production == "True":
    app = create_app()
else:
    app = create_app(Production_Config)

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=10)
def check_courses():
    print('course check job running')
    with app.app_context():
        courses = CourseModel.query.all()
        for course in courses:
            if course.should_start():
                course.start()
            if course.should_end():
                course.end()
            if course.should_cancel():
                course.cancel()

sched.start()
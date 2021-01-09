from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from TUTOR.config import Config
from flask_migrate import Migrate



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users_blueprint.login'
login_manager.login_message_category = "info"
mail = Mail()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)


    from TUTOR.MAIN.routes import main_blueprint
    from TUTOR.TUTORS.routes import tutors_blueprint
    from TUTOR.STUDENTS.routes import students_blueprint
    from TUTOR.ADMINISTRATION.routes import admins_blueprint
    from TUTOR.USERS.routes import users_blueprint
    from TUTOR.COURSES.routes import courses_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(tutors_blueprint)
    app.register_blueprint(students_blueprint)
    app.register_blueprint(admins_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(courses_blueprint)

    return app
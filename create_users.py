from TUTOR import db, create_app
from TUTOR.models import UserModel
from TUTOR.models import StudentDataModel, TutorDataModel
from TUTOR.config import Production_Config
from TUTOR import bcrypt
from datetime import datetime
import sys
import os

arguments = sys.argv
if (len(arguments) != 2) or (int(arguments[1]) != 1 and int(arguments[1]) != 2):
    print("usage: create_first_admin.py <1 for production | 2 for local>") 
    sys.exit(2)

app = None
server_version = int(sys.argv[1])

if server_version == 1:
   pass
elif server_version == 2:
    app = create_app()
    app.app_context().push()
    # student
    first_name = "Ammar"
    last_name = "almuwallad"
    username = "almuwallad"
    email = "gbeast123488@gmail.com"
    password = bcrypt.generate_password_hash("almowld12").decode("utf-8")
    user_type = "student"
    gender = True
    is_confirmed = True
    user = UserModel(first_name=first_name, last_name=last_name, username=username, email=email, password=password, user_type=user_type, is_confirmed=is_confirmed, _gender=gender)
    db.session.add(user)
    db.session.commit()
    student_data_model = StudentDataModel(user_id=user.id, date_of_birth=datetime.date(datetime.utcnow()))
    db.session.add(student_data_model)
    db.session.commit()
    # tutor
    first_name = "Ammar"
    last_name = "almuwallad"
    username = "xstayhighx4"
    email = "albrns1123488@outlook.com"
    password = bcrypt.generate_password_hash("almowld12").decode("utf-8")
    user_type = "tutor"
    gender = True
    is_confirmed = True
    user = UserModel(first_name=first_name, last_name=last_name, username=username, email=email, password=password, user_type=user_type, is_confirmed=is_confirmed, _gender=gender)
    db.session.add(user)
    db.session.commit()
    tutor_data_model = TutorDataModel(user_id=user.id, date_of_birth=datetime.date(datetime.utcnow()), nationality="dwafwf", qualification="dwafwaf",
    major="dwadwd", current_job="dwadw", _subjects='["math"]', years_of_experience=4, _tools_used_for_online_tutoring='["zoom"]',
    max_classes_per_day=7, min_classes_per_day=2, most_convenietnt_periods="[16, 17, 18]")
    db.session.add(tutor_data_model)
    db.session.commit()




print("DONE")




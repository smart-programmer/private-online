from TUTOR import db, create_app
from TUTOR.USERS.models import UserModel
from TUTOR.ADMINISTRATION.models import AdminDataModel
from TUTOR.config import Production_Config
from TUTOR import bcrypt
import sys
import os

arguments = sys.argv
if len(arguments != 2) or (arguments[1] != 1 and arguments[1] != 2):
    print("usage: program.py <1 for production | 2 for local>") 
    sys.exit(2)

if arguments[1] == 1:
    app = create_app(Production_Config)
elif arguments[1] == 2:
    app = create_app()

app.app_context().push()

first_name = "Ammar"
last_name = "almuwallad"
username = os.environ["admin_username"]
email = os.environ["admin_email"]
password = bcrypt.generate_password_hash(os.environ["admin_password"]).decode("utf-8")
user_type = "admin2"
is_confirmed = True

user = UserModel(first_name=first_name, last_name=last_name, username=username, email=email, password=password, user_type=user_type, is_confirmed=is_confirmed)
db.session.add(user)
db.session.commit()
admin_data_model = AdminDataModel(user_id=user.id)
db.session.add(admin_data_model)
db.session.commit()




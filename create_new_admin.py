from TUTOR import db, create_app
from TUTOR.models import UserModel
from TUTOR.models import AdminDataModel
from TUTOR.config import Production_Config
from TUTOR import bcrypt
import sys
import os

arguments = sys.argv
if ((len(arguments) != 2) or (int(arguments[1]) != 1 and int(arguments[1]) != 2)):
    print("usage: create_first_admin.py <1 for production | 2 for local>") 
    sys.exit(2)

app = None
server_version = int(sys.argv[1])

if server_version == 1:
    app = create_app(Production_Config)
    first_name = "placeholder"
    last_name = "placeholder"
    username = "placeholder"
    email = "placeholder"
    password = bcrypt.generate_password_hash("placeholder").decode("utf-8")
    user_type = "admin1"
    gender = True
    is_confirmed = True
elif server_version == 2:
    app = create_app()
    first_name = "placeholder"
    last_name = "placeholder"
    username = "placeholder"
    email = "placeholder"
    password = bcrypt.generate_password_hash("admin").decode("utf-8")
    user_type = "admin1"
    gender = True
    is_confirmed = True

print(arguments[1] )
app.app_context().push()



user = UserModel(first_name=first_name, last_name=last_name, username=username, email=email, password=password, user_type=user_type, is_confirmed=is_confirmed, _gender=gender)
db.session.add(user)
db.session.commit()
admin_data_model = AdminDataModel(user_id=user.id)
db.session.add(admin_data_model)
db.session.commit()
print("DONE")




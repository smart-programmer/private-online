import sys
from TUTOR import create_app, db
from TUTOR.config import Production_Config
from TUTOR.models import SiteSettingsModel
import json

if len(sys.argv) != 2:
    print("usage: create_site.py <1 for production | 2 for local>") 
    sys.exit()
    
server_version = int(sys.argv[1])
print(server_version)

if server_version != 2 and server_version != 1:
    print("usage: create_site.py <1 for production | 2 for local>") 
    sys.exit()


if server_version == 1:
    app = create_app(config_class=Production_Config)
else:
    app = create_app()

app.app_context().push()

default_settings_dict = {
    "allow_tutors_to_create_courses" : {"setting_type": bool.__name__, 'setting_value': True},
    "allow_tutors_to_edit_courses": {"setting_type": bool.__name__, 'setting_value': True},
    "subjects": {"setting_type": list.__name__, 'setting_value': ["math", "english", "physics"]}
}

deafult_settings_model = SiteSettingsModel(_settings=json.dumps(default_settings_dict)) #  "allow_tutors_to_create_courses", value="True"
# setting2 = SiteSettingsModel(name="allow_tutors_to_edit_courses", value="True")
# setting3 = SiteSettingsModel(name="allowed_subject", value="Math")
# setting4 = SiteSettingsModel(name="allowed_subject", value="Physics")


# db.session.add(setting1)
# db.session.add(setting2)
# db.session.add(setting3)
# db.session.add(setting4)
db.session.add(deafult_settings_model)
db.session.commit()

print("Done")
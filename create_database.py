from TUTOR import create_app, db
from TUTOR.config import Production_Config, SQLITE_VARIABLE
import sys
import os 


arguments = sys.argv
if (len(arguments) != 2) or (int(arguments[1]) != 1 and int(arguments[1]) != 2):
    print("usage: drop_database.py <1 for production | 2 for local>") 
    sys.exit(2)


server_version = int(sys.argv[1])
app = None
if server_version == 1:
    app = create_app(config_class=Production_Config)
    app.app_context().push()
    db.drop_all()
else:
    app = create_app()
    app.app_context().push()
    db.drop_all()
    os.remove(app.config.get("SQLALCHEMY_DATABASE_URI").replace(SQLITE_VARIABLE, ""))


print("DONE")
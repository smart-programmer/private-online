from TUTOR import create_app
from TUTOR.config import Production_Config
from flask_migrate import MigrateCommand, Manager
import sys
import os


production_var = os.environ.get("production")


app = None
if production_var in ("True", "true"):
    app = create_app(config_class=Production_Config)
else:
    app = create_app()

manager = Manager(app)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
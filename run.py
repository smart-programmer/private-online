from TUTOR import create_app, db
from TUTOR.config import Production_Config
from TUTOR.models import SiteSettingsModel
import os 
import sys

if os.environ.get("production"):
     app = create_app(config_class=Production_Config)
else:
     app = create_app()

with app.app_context():
     if len(SiteSettingsModel.query.all()) < 1:
          settings = SiteSettingsModel()
          db.session.add(settings)
          db.session.commit()

if __name__ == "__main__":
     app.run(debug=True)

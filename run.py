from SPORT import create_app
from SPORT.config import Production_Config
import os 
import sys

if os.environ.get("production"):
     app = create_app(config_class=Production_Config)
else:
     app = create_app()


if __name__ == "__main__":
     app.run(debug=True)

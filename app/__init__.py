from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_principal import Principal
from flask_mail import Mail

load_dotenv()
app = Flask(__name__)

IDOC_USER = os.getenv('IDOC_USER')
IDOC_PWD = os.getenv('IDOC_PWD')
IDOC_HOST = os.getenv('IDOC_HOST')
IDOC_DB = os.getenv('IDOC_DB')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{IDOC_USER}:{IDOC_PWD}@{IDOC_HOST}/{IDOC_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ad983778da711747f7cb3e3b'
db = SQLAlchemy(app)

bcrypt= Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"

principal = Principal(app)


app.config['MAIL_SERVER']=os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] =False
mail = Mail(app)

from app.views import main
from app.views import patient
from app.views import test

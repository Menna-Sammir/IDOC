from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_principal import Principal
import uuid

load_dotenv()
app = Flask(__name__)

IDOC_USER = os.getenv('IDOC_USER')
IDOC_PWD = os.getenv('IDOC_PWD')
IDOC_HOST = os.getenv('IDOC_HOST')
IDOC_DB = os.getenv('IDOC_DB')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{IDOC_USER}:{IDOC_PWD}@{IDOC_HOST}/{IDOC_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ad983778da711747f7cb3e3b'
db = SQLAlchemy(app)
app.config['CACHE_ID'] = str(uuid.uuid4())

bcrypt= Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"

principal = Principal(app)



from app.views import main
from app.views import patient

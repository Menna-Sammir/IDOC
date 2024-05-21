from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

IDOC_USER = os.getenv('IDOC_USER')
IDOC_PWD = os.getenv('IDOC_PWD')
IDOC_HOST = os.getenv('IDOC_HOST')
IDOC_DB = os.getenv('IDOC_DB')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{IDOC_USER}:{IDOC_PWD}@{IDOC_HOST}/{IDOC_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

from app.views import home

from flask import Flask, request, redirect, url_for, session
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_principal import Principal
import uuid
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_babel import Babel
import json
from babel import dates


load_dotenv()
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
babel = Babel(app)

IDOC_USER = os.getenv('IDOC_USER')
IDOC_PWD = os.getenv('IDOC_PWD')
IDOC_HOST = os.getenv('IDOC_HOST')
IDOC_DB = os.getenv('IDOC_DB')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{IDOC_USER}:{IDOC_PWD}@{IDOC_HOST}/{IDOC_DB}'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{IDOC_USER}:{IDOC_PWD}@{IDOC_HOST}/{IDOC_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ad983778da711747f7cb3e3b'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ar']


def load_translations(translations):
    try:
        with open(translations, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{translations}' not found.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{translations}': {e}")
        return {}

translations = load_translations('translations.json')


def get_locale():
    return session.get('lang', request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES']))

def translate(key):
    lang = get_locale()
    translation = translations.get(lang, {}).get(key, key)
    return translation


def lazy_translate(key):
    return lambda: translate(key)

@app.route('/set_language')
def set_language():
    language = request.args.get('language', 'en')
    if language in ['en', 'ar']:
        session['lang'] = language
    return redirect(request.referrer or url_for('index'))

@app.context_processor
def inject_translations():
    return dict(get_locale=get_locale, translate=translate)



db = SQLAlchemy(app)
app.config['CACHE_ID'] = str(uuid.uuid4())

#Configure flask_bcrypt
bcrypt= Bcrypt(app)

#Configure flask_login
login_manager = LoginManager(app)
login_manager.login_view = "login_page"

# Configure Flask-Uploads
app.config['UPLOAD_FOLDER'] = os.path.join('app','static', 'images')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

directory = 'app/static/images/'
os.chmod(directory, 0o755)


csrf = CSRFProtect(app)
#Configure flask_principal
principal = Principal(app)



from app.views import main
from app.views import doctor
from app.views import admin
from app.views import patient
from app.views import clinic



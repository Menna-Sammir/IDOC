from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_principal import Principal
from flask_uploads import UploadSet, IMAGES, configure_uploads
import uuid
from flask_wtf.csrf import CSRFProtect



load_dotenv()
app = Flask(__name__)

IDOC_USER = os.getenv('IDOC_USER')
IDOC_PWD = os.getenv('IDOC_PWD')
IDOC_HOST = os.getenv('IDOC_HOST')
IDOC_DB = os.getenv('IDOC_DB')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{IDOC_USER}:{IDOC_PWD}@{IDOC_HOST}/{IDOC_DB}'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{IDOC_USER}:{IDOC_PWD}@{IDOC_HOST}/{IDOC_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'ad983778da711747f7cb3e3b'
# app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.getcwd(), 'uploads')


db = SQLAlchemy(app)

app.config['CACHE_ID'] = str(uuid.uuid4())

app.config['Current_user'] = current_user

#Configure flask_bcrypt
bcrypt= Bcrypt(app)

#Configure flask_login
login_manager = LoginManager(app)
login_manager.login_view = "login_page"

# Configure Flask-Uploads
# photos = UploadSet('images', IMAGES)
app.config['UPLOAD_FOLDER'] = os.path.join('app','static', 'images')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

directory = 'app/static/images/'
os.chmod(directory, 0o755)


csrf = CSRFProtect(app)
#Configure flask_principal
principal = Principal(app)



from app.views import main
from app.views import patient

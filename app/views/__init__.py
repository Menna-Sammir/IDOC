from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/app')

from app.views.main import *

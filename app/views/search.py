from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models.models import User, Doctor
from app.models.models import Specialization
from app.models.models import Governorate
from app.models.models import Doctor

class SearchForm(FlaskForm):
    specialization = SelectField('Specialization', choices=[], validators=[DataRequired()])
    governorate = SelectField('Governorate', choices=[], validators=[DataRequired()])
    doctor_name = StringField('Doctor Name')
    submit = SubmitField('Search')

from flask_principal import Permission, RoleNeed
from app.models.models import *
from wtforms import  SubmitField, SelectField
from flask_wtf import FlaskForm
from app.views.booking import AppointmentForm

class bookdoc(FlaskForm):
    timeslots = SelectField('Choose a time slot', choices=[])
    submit = SubmitField('Book Appointment')
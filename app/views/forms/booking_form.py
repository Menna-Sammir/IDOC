from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

class AppointmentForm(FlaskForm):
    timeslots = RadioField('Available Timeslots', choices=[], validators=[DataRequired()])
    submit = SubmitField('Continue')
    
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from app import translate

class AppointmentForm(FlaskForm):
    timeslots = RadioField('Available Timeslots', choices=[], validators=[DataRequired()])
    submit = SubmitField('Continue')
    
def translate_labels(self):
    self.timeslots.label.text = translate('Available Timeslots')
    self.submit.label.text = translate('Continue')
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, HiddenField
from wtforms.validators import DataRequired
<<<<<<< HEAD
=======
from app import translate
>>>>>>> 43f670543734e42f1cbe595ce9a8b1d215f97291

class AppointmentForm(FlaskForm):
    timeslots = RadioField('Available Timeslots', choices=[], validators=[DataRequired()])
    submit = SubmitField('Continue')
<<<<<<< HEAD
=======
    
def translate_labels(self):
    self.timeslots.label.text = translate('Available Timeslots')
    self.submit.label.text = translate('Continue')
>>>>>>> 43f670543734e42f1cbe595ce9a8b1d215f97291

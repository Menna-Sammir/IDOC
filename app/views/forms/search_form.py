from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app import translate

class SearchForm(FlaskForm):
    specialization = SelectField(validators=[DataRequired()])
    governorate = SelectField(validators=[DataRequired()])
    doctor_name = StringField()
    submit = SubmitField('')
    
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.specialization.label.text = translate('Specialization')
        self.governorate.label.text = translate('Governorate')
        self.doctor_name.label.text = translate('Doctor Name')
        
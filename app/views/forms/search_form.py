from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
<<<<<<< HEAD


class SearchForm(FlaskForm):
    specialization = SelectField('Specialization', choices=[], validators=[DataRequired()])
    governorate = SelectField('Governorate', choices=[], validators=[DataRequired()])
    doctor_name = StringField('Doctor Name')
    submit = SubmitField('')
=======
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
        
>>>>>>> 43f670543734e42f1cbe595ce9a8b1d215f97291

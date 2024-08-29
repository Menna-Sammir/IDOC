from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    specialization = SelectField('Specialization', choices=[], validators=[DataRequired()])
    governorate = SelectField('Governorate', choices=[], validators=[DataRequired()])
    doctor_name = StringField('Doctor Name')
    submit = SubmitField('')

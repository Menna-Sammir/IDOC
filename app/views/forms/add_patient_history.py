from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired
from app.models.models import PatientHisType
from enum import Enum

class PatientHistoryForm(FlaskForm):
    details = FileField('Upload Details', validators=[FileRequired()])
    
    type = SelectField(
        'Select Type',
        choices=[(choice.name, choice.value) for choice in PatientHisType],
        validators=[DataRequired()]
    )
    
    submit = SubmitField('Upload')

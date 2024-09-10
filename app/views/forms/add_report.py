from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from werkzeug.utils import secure_filename
import os

class AddReportForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    diagnosis = TextAreaField('Diagnosis', validators=[DataRequired()])
    report_file = FileField('Upload Report (PDF only)', validators=[DataRequired()])
    appointment_id = HiddenField('Appointment ID')
    patient_id = HiddenField('Patient ID')
    submit = SubmitField('Submit')
    
    def validate_report_file(self, field):
        if field.data:
            filename = secure_filename(field.data.filename)
            if not filename.endswith('.pdf'):
                raise ValidationError('Only PDF files are allowed.')

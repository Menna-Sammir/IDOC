from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models.models import *
from wtforms_components import TimeField
from flask_wtf.file import FileField
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect()
class ClinicForm(FlaskForm):

    def validate_email_address(self, email_address_to_check, clinicName):
        email_address = Clinic.query.filter_by(email= email_address_to_check.data).first()
        if email_address:
            raise ValidationError('email address already exists!')
        clinic = Clinic.query.filter_by(name= clinicName.data).first()
        if clinic:
            raise ValidationError('clinic already exists!')

    def file_size_check(self, logo):
        if logo.data:
            if len(logo.data.read()) > 2 * 1024 * 1024:
                raise ValidationError('File size must be less than 2MB.')
            logo.data.seek(0)

    clinicName =StringField(label='Clinic Name', validators=[Length(min=2,max=30), DataRequired()])
    clinicAddress =TextAreaField(label='Clinic Address', validators=[Length(min=2,max=90), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired(),Length(max=50)])
    gov_id = SelectField(label='governorate', validators=[DataRequired()])
    phone = StringField(label='Phone', validators=[Length(min=11, max=11)])
    fromHour=TimeField(label='From', validators=[DataRequired()])
    toHour=TimeField(label='To', validators=[DataRequired()])
    logo=FileField(label='Clinic Logo', validators=[DataRequired(),file_size_check])

    submit = SubmitField(label='Add Clinic')

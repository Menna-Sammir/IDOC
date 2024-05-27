from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length, Email, DataRequired, ValidationError
from flask_wtf.file import FileField
from flask_wtf.csrf import CSRFProtect
from app.models.models import *

csrf = CSRFProtect()
class DoctorForm(FlaskForm):
    def email_address(self, email_address_to_check, clinic_id):
        email_address = Clinic.query.filter_by(email= email_address_to_check.data).first()
        if email_address:
            raise ValidationError('email address already exists!')
        clinic = Clinic.query.filter_by(id= clinic_id.data).first()
        if clinic:
            raise ValidationError('clinic already exists!')

    def file_size_check(self, photo):
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if photo.data:
            if len(photo.data.read()) > 2 * 1024 * 1024:
                raise ValidationError('File size must be less than 2MB.')
            photo.data.seek(0)
            filename = photo.data.filename
            if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                raise ValidationError('Unsupported file extension.')

    firstname =StringField(label='First Name', validators=[Length(min=2,max=30), DataRequired()])
    lastname =StringField(label='Last Name', validators=[Length(min=2,max=70), DataRequired()])
    price =StringField(label='pricing', validators=[Length(min=2,max=90), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired(), Length(max=50)])
    phone = StringField(label='Phone', validators=[Length(min=0, max=11)])
    photo = FileField(label='Doctor Image', validators=[DataRequired(), file_size_check])
    clinic_id = SelectField(label='governorate', validators=[DataRequired()])
    specialization_id = SelectField(label='governorate', validators=[DataRequired()])
    submit = SubmitField(label='Add Doctor')

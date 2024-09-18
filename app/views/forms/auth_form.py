from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, SelectField, RadioField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models.models import *
import re
from flask_wtf.file import FileField

class RegisterForm(FlaskForm):
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email= email_address_to_check.data).first()
        if email_address:
            raise ValidationError('email address already exists!')

    username =StringField(label='User Name', validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    phone = StringField(validators=[Length(min=0, max=11), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    def validate_email_or_id(form, field):
        email_regex = r'^\S+@\S+\.\S+$'
        id_regex = r'^\d{6,10}$'

        if not re.match(email_regex, field.data) and not re.match(id_regex, field.data):
            raise ValidationError('Input must be a valid email address or a valid ID number.')

    email_address = StringField(label='Email Address:', validators=[validate_email_or_id, DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='log in')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')

class ResetPasswordForm(FlaskForm):
    Temp_password = PasswordField('temporary Password', validators=[DataRequired()])
    new_password = PasswordField('Password', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('set Password')


class AppointmentForm(FlaskForm):
    timeslots = RadioField('Available Timeslots', choices=[], validators=[DataRequired()])
    submit = SubmitField('Book Appointment')



class EditUserForm(FlaskForm):
    def validate_email_address(self, email_address_to_check):
        email = User.query.filter_by(email= email_address_to_check.data).first()
        if email:
            raise ValidationError('email address already exists!')

    def file_size_check(self, photo):
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if photo.data:
            if len(photo.data.read()) > 2 * 1024 * 1024:
                raise ValidationError(translate('File size must be less than 2MB.'))
            photo.data.seek(0)
            filename = photo.data.filename
            if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                raise ValidationError(translate('Unsupported file extension.'))


    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    photo = FileField(validators=[file_size_check])


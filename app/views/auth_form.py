from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models.models import User, Doctor

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username= username_to_check.data).first()
        if user:
            raise ValidationError('username already exists!')

    def validate_doctor(self, doctor_to_check):
        doctor = Doctor.query.filter_by(name= doctor_to_check.data).first()
        if not doctor:
            raise ValidationError('doctor not exists!')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address= email_address_to_check.data).first()
        if email_address:
            raise ValidationError('email address already exists!')


    username =StringField(label='User Name', validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    doctor = SelectField(label='select doctor', validators=[DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='sign in')

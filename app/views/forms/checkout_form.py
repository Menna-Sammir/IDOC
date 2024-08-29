from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models.models import *


class checkoutForm(FlaskForm):

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email= email_address_to_check.data).first()
        if email_address:
            raise ValidationError('email address already exists!')

    firstname =StringField(label='First Name', validators=[Length(min=2,max=30), DataRequired()])
    lastname =StringField(label='Last Name', validators=[Length(min=2,max=70), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    phone = StringField(label='Phone', validators=[Length(min=11, max=11)])
<<<<<<< HEAD
    submit = SubmitField(label='Confirm Book')
=======
    submit = SubmitField(label='Confirm Book')
>>>>>>> 7af7b32b47e5e71ee9efd83e617a0680a8819b9e

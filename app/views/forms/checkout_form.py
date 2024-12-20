from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models.models import *
from app import translate


class checkoutForm(FlaskForm):
    firstname = StringField(validators=[Length(min=2, max=30), DataRequired()])
    lastname = StringField(validators=[Length(min=2, max=70), DataRequired()])
    email_address = StringField(validators=[Email(), DataRequired()])
    phone = StringField(validators=[Length(min=0, max=11)])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(checkoutForm, self).__init__(*args, **kwargs)
        self.firstname.label.text = translate('First Name')
        self.lastname.label.text = translate('Last Name')
        self.email_address.label.text = translate('Email Address')
        self.phone.label.text = translate('Phone')
        self.submit.label.text = translate('Confirm Book')

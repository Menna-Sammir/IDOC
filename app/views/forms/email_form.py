from flask_wtf import FlaskForm
<<<<<<< HEAD
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError


class EmailForm(FlaskForm):
    name =StringField(label='Name', validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    subject = StringField(label='Subject', validators=[Length(min=2, max=20), DataRequired()])
    message = TextAreaField(label='Message', validators=[Length(min=2, max=1000), DataRequired()])
    submit = SubmitField(label='send message')
=======
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, Email, DataRequired
from app import translate

class EmailForm(FlaskForm):
    name = StringField(validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(validators=[Email(), DataRequired()])
    subject = StringField(validators=[Length(min=2, max=20), DataRequired()])
    message = TextAreaField(validators=[Length(min=2, max=1000), DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.name.label.text = translate('Name')
        self.email_address.label.text = translate('Email Address')
        self.subject.label.text = translate('Subject')
        self.message.label.text = translate('Message')
        self.submit.label.text = translate('Send Message')
>>>>>>> 43f670543734e42f1cbe595ce9a8b1d215f97291

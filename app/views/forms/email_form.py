from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError


class EmailForm(FlaskForm):
    name =StringField(label='Name', validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    subject = StringField(label='Subject', validators=[Length(min=2, max=20), DataRequired()])
    message = TextAreaField(label='Message', validators=[Length(min=2, max=1000), DataRequired()])
    submit = SubmitField(label='send message')
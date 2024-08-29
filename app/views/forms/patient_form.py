from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, FileField
from wtforms.validators import Length, Email, DataRequired, ValidationError
from app.models.models import User, BloodGroup, Governorate, Allergy
import os

class PatientForm(FlaskForm):
    
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.governorate.choices = [(g.id, g.governorate_name) for g in Governorate.query.all()]
        self.blood_group.choices = [(bg.name, bg.value) for bg in BloodGroup]
        self.allergy.choices = [(a.name, a.value) for a in Allergy]

    def validate_email_address(self, field):
        email_address = User.query.filter_by(email=field.data).first()
        if email_address:
            raise ValidationError('Email address already exists!')
        
    def validate_photo(self, field):
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if field.data:
            field.data.seek(0, os.SEEK_END)
            file_size = field.data.tell()
            field.data.seek(0)
            if file_size > 2 * 1024 * 1024:
                raise ValidationError('File size must be less than 2MB.')
            filename = field.data.filename
            if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                raise ValidationError('Unsupported file extension.')
            
    firstname = StringField('First Name', validators=[Length(min=2, max=30), DataRequired()])
    lastname = StringField('Last Name', validators=[Length(min=2, max=70), DataRequired()])
    email = StringField('Email Address', validators=[Email(), DataRequired(), Length(max=50)])
    phone = StringField('Phone', validators=[Length(min=0, max=11)])
    photo = FileField('Photo', validators=[validate_photo])
    address = TextAreaField('Address', validators=[DataRequired()])
    governorate = SelectField('Governorate', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    blood_group = SelectField('Blood Group', validators=[DataRequired()])
    allergy = SelectField('Allergy', validators=[DataRequired()])


    submit = SubmitField('Submit')

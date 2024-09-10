
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models.models import User
from flask_wtf.file import FileField
from flask_wtf.csrf import CSRFProtect
from app import translate

csrf = CSRFProtect()

def file_size_check(self, logo):
        if logo.data:
            if len(logo.data.read()) > 2 * 1024 * 1024:
                raise ValidationError(translate('File size must be less than 2MB.'))
            logo.data.seek(0)

class ClinicForm(FlaskForm):


    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email=email_address_to_check.data).first()
        if email_address:
            raise ValidationError(translate('email address already exists!'))

    def file_size_check(self, logo):
        if logo.data:
            if len(logo.data.read()) > 2 * 1024 * 1024:
                raise ValidationError(translate('File size must be less than 2MB.'))
            logo.data.seek(0)

    clinicName = StringField(validators=[Length(min=2, max=30), DataRequired()])
    clinicAddress = TextAreaField(validators=[Length(min=2, max=90), DataRequired()])
    email_address = StringField(validators=[Email(), DataRequired(), Length(max=50)])
    gov_id = SelectField(validators=[DataRequired()])
    phone = StringField(validators=[Length(min=0, max=11)])
    logo = FileField(validators=[DataRequired(), file_size_check])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(ClinicForm, self).__init__(*args, **kwargs)
        self.translate()

    def translate(self):
        self.clinicName.label.text = translate('Clinic Name')
        self.clinicAddress.label.text = translate('Clinic Address')
        self.email_address.label.text = translate('Email Address')
        self.gov_id.label.text = translate('governorate')
        self.phone.label.text = translate('Phone')
        self.logo.label.text = translate('Clinic Logo')
        self.submit.label.text = translate('Add Clinic')

class EditClinicForm(FlaskForm):

    name = StringField(validators=[Length(min=2, max=30), DataRequired()])
    address = TextAreaField(validators=[Length(min=2, max=90), DataRequired()])
    phone = StringField(validators=[Length(min=0, max=11)])
    gov_id = SelectField(validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(EditClinicForm, self).__init__(*args, **kwargs)
        self.translate()

    def translate(self):
        self.name.label.text = translate('Clinic Name')
        self.address.label.text = translate('Clinic Address')
        self.phone.label.text = translate('phone number')
        self.gov_id.label.text = translate('governorate')
        self.submit.label.text = translate('Add Clinic')

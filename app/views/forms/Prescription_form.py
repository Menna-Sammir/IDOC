<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from flask_wtf import FlaskForm
from wtforms import widgets
from wtforms import FormField, FieldList, StringField, IntegerField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired
from app.models.models import MedicineTime


class MedicineForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    Days = IntegerField('Days', validators=[DataRequired()])
    time_of_day = SelectMultipleField(
        'Time',
        choices=[(time.name, time.value) for time in MedicineTime],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )



class AddMedicineForm(FlaskForm):
    items = FieldList(FormField(MedicineForm), min_entries=1, max_entries=10)
    submit = SubmitField('Submit')
=======
=======
>>>>>>> b1ada92490b7c46372fbf52fc152dd4c8744177f
=======
>>>>>>> b1ada92490b7c46372fbf52fc152dd4c8744177f
from flask_wtf import FlaskForm
from wtforms import widgets
from wtforms import FormField, FieldList, StringField, IntegerField, SelectMultipleField, SubmitField
=======
from flask_wtf import FlaskForm
from wtforms import FormField, FieldList, StringField, IntegerField, SelectMultipleField, SubmitField, HiddenField, widgets
>>>>>>> 8dec8cef8230cc6629b6bd6992c7542cc2364b7b
from wtforms.validators import DataRequired
from app.models.models import MedicineTime


class MedicineForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    Days = IntegerField('Days', validators=[DataRequired()])
    time_of_day = SelectMultipleField(
        'Time',
        choices=[(time.name, time.value) for time in MedicineTime],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )



class AddMedicineForm(FlaskForm):
    items = FieldList(FormField(MedicineForm), min_entries=1, max_entries=10)
<<<<<<< HEAD
    submit = SubmitField('Submit')
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> b1ada92490b7c46372fbf52fc152dd4c8744177f
=======
>>>>>>> b1ada92490b7c46372fbf52fc152dd4c8744177f
=======
>>>>>>> b1ada92490b7c46372fbf52fc152dd4c8744177f
=======
    patient_id = HiddenField("patient_id")
    submit = SubmitField('Submit')
>>>>>>> 8dec8cef8230cc6629b6bd6992c7542cc2364b7b

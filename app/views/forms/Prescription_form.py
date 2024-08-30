from flask_wtf import FlaskForm
from wtforms import FormField, FieldList, StringField, IntegerField, SelectMultipleField, SubmitField, HiddenField, widgets
from wtforms.validators import DataRequired
from app.models.models import MedicineTime


class MedicineForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    time_of_day = SelectMultipleField(
        'Time',
        choices=[(time.name, time.value) for time in MedicineTime],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )



class AddMedicineForm(FlaskForm):
    items = FieldList(FormField(MedicineForm), min_entries=1, max_entries=10)
    patient_id = HiddenField("patient_id")
    submit = SubmitField('Submit')

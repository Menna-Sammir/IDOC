from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models.models import Specialization, Doctor, Clinic, Governorate, Patient
from flask_principal import Permission, RoleNeed
from werkzeug.utils import secure_filename
import uuid
from app.views.forms.addClinic_form import ClinicForm
from app.views.forms.addDoctor_form import DoctorForm
import os
from app import translate


admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# admin dashboard page >>> view appointments today
@app.route(
    '/admin_dashboard',
    methods=['GET', 'POST'],
    strict_slashes=False,
    endpoint='dashboard'
)
@login_required
# @admin_permission.require(http_exception=403)
def admin_dash():
    doctor_details = db.session.query(Doctor).all()
    clinic_details = db.session.query(Clinic).all()
    doctor_count = db.session.query(Doctor).count()
    clinic_count = db.session.query(Clinic).count()
    patient_count = db.session.query(Patient).count()
    return render_template(
        'admin-dashboard.html',
        doctor_details=doctor_details,
        clinic_details=clinic_details,
        doctor_count=doctor_count,
        clinic_count=clinic_count,
        patient_count=patient_count
    )


@login_required
# @admin_permission.require(http_exception=403)
@app.route(
    '/add_clinic', methods=['GET', 'POST'], strict_slashes=False, endpoint='add_clinic'
)
def add_clinic():
    add_clinic_form = ClinicForm()
    govs = Governorate.query.filter().all()
    add_clinic_form.gov_id.choices = [('', translate('Select a governorate'))] + [
        (gov.id, translate(gov.governorate_name)) for gov in govs
    ]
    if request.method == 'POST':
        try:
            clinic = Clinic.query.filter_by(
                name=add_clinic_form.clinicName.data
            ).first()

            if clinic:
                flash(translate('clinic already exists!'))
            else:
                if add_clinic_form.validate_on_submit():

                    Clinic_create = Clinic(
                        name=add_clinic_form.clinicName.data,
                        phone=add_clinic_form.phone.data,
                        email=add_clinic_form.email_address.data,
                        address=add_clinic_form.clinicAddress.data,
                        governorate_id=add_clinic_form.gov_id.data
                    )

                    if 'logo' not in request.files:
                        flash(translate('No file part'))
                        return redirect(request.url)
                    file = request.files['logo']
                    if file.filename == '':
                        flash(translate('No selected file'))
                        return redirect(request.url)
                    unique_str = str(uuid.uuid4())[:8]
                    original_filename, extension = os.path.splitext(file.filename)
                    new_filename = f"{unique_str}_{add_clinic_form.clinicName.data.replace(' ', '_')}{extension}"
                    Clinic_create.photo = new_filename

                    if file and allowed_file(file.filename):
                        filename = secure_filename(new_filename)
                        file.save(
                            os.path.join(
                                app.config['UPLOAD_FOLDER'], 'clinic', filename
                            )
                        )
                    db.session.add(Clinic_create)
                    db.session.commit()
                    return redirect(url_for('dashboard'))
                if add_clinic_form.errors != {}:
                    for err_msg in add_clinic_form.errors.values():
                        flash(
                            f'there was an error with creating a user: {err_msg}',
                            category='danger'
                        )
        except Exception as e:
            flash(f'something wrong', category='danger')
            print(str(e))
    return render_template('add-clinic.html', form=add_clinic_form)


@login_required
# @admin_permission.require(http_exception=403)
@app.route(
    '/add_doctor', methods=['GET', 'POST'], strict_slashes=False, endpoint='add_doctor'
)
def add_doctor():
    add_doctor_form = DoctorForm()
    clinics = Clinic.query.filter().all()
    specializations = Specialization.query.filter().all()
    add_doctor_form.clinic_id.choices = [('', translate('Select a clinic'))] + [
        (clinic.id, translate(clinic.name)) for clinic in clinics
    ]
    add_doctor_form.specialization_id.choices = [('', translate('Select a specialization'))] + [
        (specialization.id, translate(specialization.specialization_name))
        for specialization in specializations
    ]
    if request.method == 'POST':
        if add_doctor_form.validate_on_submit():
            doctor_name = (
                add_doctor_form.firstname.data + ' ' + add_doctor_form.lastname.data
            )
            doctor = Doctor.query.filter_by(
                name=doctor_name, clinic_id=add_doctor_form.clinic_id.data
            ).first()

            if doctor:
                flash(translate('doctor already exists!'))
            else:
                try:
                    clinic = Clinic.query.get(add_doctor_form.clinic_id.data).name
                    Doctor_create = Doctor(
                        name=doctor_name,
                        phone=add_doctor_form.phone.data,
                        email=add_doctor_form.email_address.data,
                        From_working_hours = add_doctor_form.fromHour.data,
                        To_working_hours = add_doctor_form.toHour.data,
                        duration = add_doctor_form.duration.data,
                        price=add_doctor_form.price.data,
                        specialization_id=add_doctor_form.specialization_id.data,
                        clinic_id=add_doctor_form.clinic_id.data,
                        iDNum=add_doctor_form.IDNum.data
                    )
                    if 'photo' not in request.files:
                        flash(translate('No file part'))
                        return redirect(request.url)
                    file = request.files['photo']
                    if file.filename == '':
                        flash(translate('No selected file'))
                        return redirect(request.url)
                    unique_str = str(uuid.uuid4())[:8]
                    original_filename, extension = os.path.splitext(file.filename)
                    new_filename = f"{unique_str}_{clinic.replace(' ', '_')}_{doctor_name.replace(' ', '_')}{extension}"
                    Doctor_create.photo = new_filename
                    if file and allowed_file(file.filename):
                        filename = secure_filename(new_filename)
                        file.save(
                            os.path.join(
                                app.config['UPLOAD_FOLDER'], 'doctors', filename
                            )
                        )
                    db.session.add(Doctor_create)
                    db.session.commit()
                    return redirect(url_for('dashboard'))
                except Exception as e:
                    flash(f'something wrong', category='danger')
        if add_doctor_form.errors != {}:
            for err_msg in add_doctor_form.errors.values():
                flash(
                    f'there was an error with adding doctor: {err_msg}',
                    category='danger'
                )
    return render_template('add-doctor.html', form=add_doctor_form)

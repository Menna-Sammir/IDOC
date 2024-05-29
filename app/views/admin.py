from app import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from datetime import datetime
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from flask_login import login_required, current_user
from flask import session
from datetime import date
from app.models.models import Specialization, User, Doctor,  Patient, Appointment, Clinic, Message,  Governorate, Role
from flask_principal import Permission, RoleNeed, Identity, AnonymousIdentity, identity_loaded, identity_changed
from werkzeug.utils import secure_filename
import uuid
from app.views.forms.addClinic_form import ClinicForm
from app.views.forms.addDoctor_form import DoctorForm
import os


admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# admin dashboard page >>> view appointments today
@app.route('/admin_dashboard', methods=['GET', 'POST'], endpoint='dashboard')
@login_required
# @admin_permission.require(http_exception=403)
def admin_dash():
    user_id = request.args.get('current_user', None)
    user = User.query.filter_by(id=user_id).first()

    doctors = db.session.query(Doctor).options(
        joinedload(Doctor.specialization),
        joinedload(Doctor.clinic)
    ).all()

    doctor_details = []
    clinic_details = set()
    for doctor in doctors:
        appointment_count = db.session.query(func.count(Appointment.id)).filter(Appointment.doctor_id == doctor.id).scalar() or 0
        total_earnings = appointment_count * (doctor.price or 0)

        details = {
            'doctor_name': doctor.name,
            'specialization': doctor.specialization.specialization_name,
            'photo': doctor.photo,
            'price': doctor.price,
            'clinic_name': doctor.clinic.name,
            'clinic_phone': doctor.clinic.phone,
            'clinic_address': doctor.clinic.address,
            'total_earnings': total_earnings
        }
        doctor_details.append(details)

        clinic_info = {
            'clinic_name': doctor.clinic.name,
            'clinic_phone': doctor.clinic.phone,
            'clinic_address': doctor.clinic.address,
            'clinic_photo': doctor.clinic.photo
        }
        clinic_details.add(frozenset(clinic_info.items()))

    clinic_details = [dict(clinic) for clinic in clinic_details]

    if request.method == 'POST':
        return redirect(url_for('logout'))

    doctor_details=db.session.query(Doctor).all()
    clinic_details=db.session.query(Clinic).all()
    doctor_count = db.session.query(Doctor).count()
    clinic_count = db.session.query(Clinic).count()
    return render_template('admin-dashboard.html',
                           doctor_details=doctor_details,
                           clinic_details=clinic_details,
                           doctor_count=doctor_count,
                           clinic_count=clinic_count)


@app.route('/add_clinic', methods=['GET', 'POST'], strict_slashes=False, endpoint='add_clinic')
def add_clinic():
    add_clinic_form = ClinicForm()
    govs = Governorate.query.filter().all()
    add_clinic_form.gov_id.choices = [('', 'Select a governorate')] + [
        (gov.id, gov.governorate_name) for gov in govs
    ]
    if request.method == 'POST':
        try:
            clinic = Clinic.query.filter_by(
                name=add_clinic_form.clinicName.data
            ).first()

            if clinic:
                flash('clinic already exists!')
            else:
                if add_clinic_form.validate_on_submit():
                    from_hour = add_clinic_form.fromHour.data.strftime('%H:%M %p')
                    to_hour = add_clinic_form.toHour.data.strftime('%H:%M %p')
                    Clinic_create = Clinic(
                        name=add_clinic_form.clinicName.data,
                        phone=add_clinic_form.phone.data,
                        email=add_clinic_form.email_address.data,
                        address=add_clinic_form.clinicAddress.data,
                        working_hours=f'from {from_hour} to {to_hour}',
                        governorate_id=add_clinic_form.gov_id.data
                    )

                    if 'logo' not in request.files:
                        flash('No file part')
                        return redirect(request.url)
                    file = request.files['logo']
                    if file.filename == '':
                        flash('No selected file')
                        return redirect(request.url)
                    unique_str = str(uuid.uuid4())[:8]
                    original_filename, extension = os.path.splitext(file.filename)
                    new_filename = (
                        f"{unique_str}_{add_clinic_form.clinicName.data}{extension}"
                    )
                    Clinic_create.photo = new_filename

                    if file and allowed_file(file.filename):
                        filename = secure_filename(new_filename)
                        file.save(
                            os.path.join(app.config['UPLOAD_FOLDER'], 'clinic', filename)
                        )

                    db.session.add(Clinic_create)
                    db.session.commit()
                    return redirect(url_for('doctor_dash'))
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


@app.route('/add_doctor', methods=['GET', 'POST'], strict_slashes=False, endpoint='add_doctor')
def add_doctor():
    add_doctor_form = DoctorForm()
    clinics = Clinic.query.filter().all()
    specializations = Specialization.query.filter().all()
    add_doctor_form.clinic_id.choices = [('', 'Select a clinic')] + [
        (clinic.id, clinic.name) for clinic in clinics
    ]
    add_doctor_form.specialization_id.choices = [('', 'Select a specialization')] + [
        (specialization.id, specialization.specialization_name)
        for specialization in specializations
    ]
    if request.method == 'POST':
        if add_doctor_form.validate_on_submit():
            doctor_name = add_doctor_form.firstname.data + ' ' + add_doctor_form.lastname.data
            doctor = Doctor.query.filter_by(
                name=doctor_name, clinic_id =add_doctor_form.clinic_id.data
            ).first()

            if doctor:
                flash('doctor already exists!')
            else:
                try:
                    clinic = Clinic.query.get(add_doctor_form.clinic_id.data).name
                    Doctor_create = Doctor(
                    name = doctor_name,
                    phone = add_doctor_form.phone.data,
                    email = add_doctor_form.email_address.data,
                    price = add_doctor_form.price.data,
                    specialization_id = add_doctor_form.specialization_id.data,
                    clinic_id = add_doctor_form.clinic_id.data
                    )
                    if 'photo' not in request.files:
                        flash('No file part')
                        return redirect(request.url)
                    file = request.files['photo']
                    if file.filename == '':
                        flash('No selected file')
                        return redirect(request.url)
                    unique_str = str(uuid.uuid4())[:8]
                    original_filename, extension = os.path.splitext(file.filename)
                    new_filename = (
                        f"{unique_str}_{clinic}_{doctor_name.strip()}{extension}"
                    )
                    Doctor_create.photo = new_filename
                    if file and allowed_file(file.filename):
                        filename = secure_filename(new_filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], "doctors", filename))
                    db.session.add(Doctor_create)
                    db.session.commit()
                    return redirect(url_for('doctor_dash'))
                except Exception as e:
                    flash(f'something wrong', category='danger')
                    print(str(e))
        if add_doctor_form.errors != {}:
            for err_msg in add_doctor_form.errors.values():
                flash(
                    f'there was an error with adding doctor: {err_msg}',
                    category='danger'
                )
    return render_template('add-doctor.html', form=add_doctor_form)

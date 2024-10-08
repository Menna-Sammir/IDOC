from app import app, db
from flask import render_template, redirect, url_for, flash, request
from datetime import datetime
from sqlalchemy import func, asc
from flask import session
from datetime import date
from app.models.models import *
from flask_principal import Permission, RoleNeed
from app.views.forms.booking_form import AppointmentForm
from app.views.forms.auth_form import EditUserForm
from app.views.forms.addDoctor_form import EditDoctorForm
from app.views.forms.Prescription_form import AddMedicineForm, MedicineForm
from flask_login import login_required, current_user
from app import translate
import os
from werkzeug.utils import secure_filename
import uuid

admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# doctor dashboard page >>> view appointments today
@app.route('/doctor_dashboard', methods=['GET', 'POST'])
@login_required
@doctor_permission.require(http_exception=403)
def doctor_dash():
    try:
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if doctor is None:
            return translate('User is not a doctor'), 403
        form = AppointmentForm()
        appointments = Appointment.query.filter_by(date=date.today(), seen=False).order_by(
            asc(Appointment.time)
        )
        if appointments.all():
            nextAppt = appointments.order_by(asc(Appointment.time)).first().id
        else:
            nextAppt = None
        monthAppointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            func.extract('month', Appointment.date) == datetime.now().month
        ).count()
        patient_count = appointments.count()
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        print(doctor)
        if doctor is None:
            return translate('User is not a doctor'), 403
        form = AppointmentForm()
        appointments = Appointment.query.filter_by(date=date.today(), seen=False).order_by(
            asc(Appointment.time)
        )
        all_appointments = Appointment.query.order_by(
        asc(Appointment.date), asc(Appointment.time)
        ).all()
        if appointments.all():
            nextAppt = appointments.order_by(asc(Appointment.time)).first().id
        else:
            nextAppt = None
        monthAppointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            func.extract('month', Appointment.date) == datetime.now().month
        ).count()
        patient_count = appointments.count()
        if request.method == 'POST':
            if 'seen' in request.form:
                appointment_id = request.form.get('appointment_id')
                appointment = Appointment.query.get(appointment_id)
                if appointment:
                    appointment.seen = True
                    appointment.status = AppStatus.Completed.value
                    db.session.commit()
                    flash('Appointment marked as seen and status updated to Completed', category='success')
                    return redirect(url_for('doctor_dash'))

        return render_template(
            'doctor-dashboard.html',
            doctor=doctor,
            appointments=appointments.all(),
            all_appointments=all_appointments,
            today=date.today(),
            patient_count=patient_count,
            monthAppointments=monthAppointments,
            nextAppt=nextAppt,
            form=form
        )
    except Exception as e:
        db.session.rollback()
        raise e


@app.route('/doctor_profile', methods=['GET', 'POST'])
@login_required
@doctor_permission.require(http_exception=403)
def doctor_profile():
    specializations = Specialization.query.filter().all()
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    user = User.query.filter_by(id=current_user.id).first_or_404()
    doctor_form = EditDoctorForm(obj=doctor)
    user_form = EditUserForm(obj=current_user)

    doctor_form.specialization_id.choices = [
        ('', translate('Select a specialization'))
    ] + [
        (specialization.id, translate(specialization.specialization_name))
        for specialization in specializations
    ]

    if request.method == 'POST':
        if doctor_form.validate_on_submit():
            try:
                doctor_form.populate_obj(doctor)
                user_form.populate_obj(user)
                user.name = (doctor_form.firstname.data + ' ' + doctor_form.lastname.data)
                doc_dur = int(doctor_form.duration.data) if doctor_form.duration.data is not None else 0
                doctor.duration = str(doc_dur * 100)
                file = request.files['photo']
                if file.filename:
                    #check from js code
                    if 'photo' in request.files:
                        unique_str = str(uuid.uuid4())[:8]
                        original_filename, extension = os.path.splitext(file.filename)
                        new_filename = f"{unique_str}_{current_user.name.replace(' ', '_')}{extension}"
                        user.photo = new_filename
                        if file and allowed_file(file.filename):
                            filename = secure_filename(new_filename)
                            file.save(
                                os.path.join(
                                    app.config['UPLOAD_FOLDER'], 'doctors', filename
                                )
                            )
                db.session.commit()
                flash('Data update successfully', category='success')
                return redirect(url_for('doctor_profile'))
            except Exception as e:
                flash(f'something wrong', category='danger')
                print(str(e))
        if doctor_form.errors != {}:
            for err_msg in doctor_form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
        elif user_form.errors != {}:
            for err_msg in user_form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
        return redirect(url_for('doctor_profile'))
    name_split = current_user.name.split()
    doctor_form.firstname.data = name_split[0]
    doctor_form.lastname.data = ' '.join(name_split[1:])
    minutes = doctor.duration.hour * 60 + doctor.duration.minute
    doctor_form.duration.data = str(minutes)
    return render_template(
        'doctor-profile-settings.html', user_form=user_form, doctor_form=doctor_form
    )


### patient list
@app.route('/patient_list', methods=['GET', 'POST'])
@login_required
def patient_list():
    clinic = Clinic.query.filter_by(user_id=current_user.id).first()
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()

    if clinic:
        patients = (
            db.session.query(Patient, User)
            .join(User, Patient.user_id == User.id)
            .join(Appointment, Appointment.patient_id == Patient.id)
            .join(Doctor, Appointment.doctor_id == Doctor.id)
            .filter(Doctor.clinic_id == clinic.id)
            .distinct(Patient.id)
            .all()
        )
    elif doctor:
        patients = (
            db.session.query(Patient, User)
            .join(User, Patient.user_id == User.id)
            .join(Appointment, Appointment.patient_id == Patient.id)
            .filter(Appointment.doctor_id == doctor.id)
            .distinct(Patient.id)
            .all()
        )
    else:
        return translate('User is not a doctor or clinic'), 403

    return render_template('patient-list.html', doctor=doctor, patients=patients)

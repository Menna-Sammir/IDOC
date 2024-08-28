from app import app, db
from flask import render_template, redirect, url_for, flash, request
from datetime import datetime
from sqlalchemy import func, asc
from flask import session
from datetime import date
from app.models.models import *
from flask_principal import Permission, RoleNeed
from app.views.forms.booking_form import AppointmentForm
from flask_login import login_required, current_user
from app import translate


admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))



# doctor dashboard page >>> view appointments today
@app.route('/doctor_dashboard', methods=['GET', 'POST'])
@login_required
@doctor_permission.require(http_exception=403)
def doctor_dash():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    print(doctor)
    if doctor is None:
        return translate('User is not a doctor'), 403
    
    form = AppointmentForm()
    appointments = Appointment.query.filter_by(date=date.today(), seen=False).order_by(asc(Appointment.time))
    if appointments.all():
        nextAppt = appointments.order_by(asc(Appointment.time)).first().id
    else:
        nextAppt = None
    monthAppointments = Appointment.query.filter(
        func.extract('month', Appointment.date) == datetime.now().month
    ).count()
    patient_count = appointments.count()

    if request.method == 'POST':
        if 'seen' in request.form:
            appointment_id = request.form.get('appointment_id')
            appointment = Appointment.query.get(appointment_id)
            if appointment:
                appointment.seen = True
                db.session.commit()
                flash('Appointment marked as seen', category='success')
                return redirect(url_for('doctor_dash'))
    return render_template(
        'doctor-dashboard.html',
        doctor=doctor,
        appointments=appointments.all(),
        patient_count=patient_count,
        monthAppointments=monthAppointments,
        nextAppt = nextAppt,
        form=form
        )


### Patient list
# @app.route('/doctor_dashboard/patient_list', methods=['GET', 'POST'])
# @login_required
# @doctor_permission.require(http_exception=403)
# def patient_list():
#     doctor = Doctor.query.filter_by(user_id=current_user.id).first()
#     if doctor is None:
#         return translate('User is not a doctor'), 403

#     appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
#     patients = [appointment.patient for appointment in appointments]
#     print("Patients:", patients)

#     return render_template('patient-list.html', doctor=doctor, patients=patients)

@app.route('/doctor_dashboard/patient_list', methods=['GET', 'POST'])
@login_required
@doctor_permission.require(http_exception=403)
def patient_list():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    if doctor is None:
        return translate('User is not a doctor'), 403

    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    patients = [appointment.patient for appointment in appointments]


    for patient in patients:
        user = User.query.filter_by(id=patient.user_id).first()
        patient.user_name = user.name if user else 'Unknown'

    return render_template('patient-list.html', doctor=doctor, patients=patients)



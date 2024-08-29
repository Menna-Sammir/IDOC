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
    user_id = current_user.id
    user = User.query.filter_by(id=user_id).first()
    print('User:', user)

    if user is None:
        return translate('User not found'), 404
    if not hasattr(user, 'doctor_id'):
        return translate('User is not a doctor'), 403
    doctor = Doctor.query.filter_by(id=user.doctor_id).first()

    if doctor is None:
        return translate('Doctor not found'), 404
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

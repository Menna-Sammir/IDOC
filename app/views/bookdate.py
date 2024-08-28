from app import app, db, principal
from flask import render_template, redirect, url_for, flash, request, current_app
from app.models.models import User, Clinic, Doctor, Role
from app.views.auth_form import RegisterDocForm, LoginForm, RegisterClinicForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import not_
from flask_principal import Permission, RoleNeed, Identity, AnonymousIdentity, identity_loaded, identity_changed
from app.models.models import *
from app.views.auth_form import LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import not_
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.models.models import Specialization, Doctor, Clinic, Governorate, Appointment
from app.views.search import SearchForm
from datetime import datetime, timedelta
from app.views.booking import AppointmentForm 
admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))

@app.route('/boooking', methods=['GET', 'POST'])
def doctor_appointments():
    form = AppointmentForm()
    doctor_id = 'doc1'
    doctor = Doctor.query.get_or_404(doctor_id)
    clinic = doctor.clinic
    dates = []
    for i in range(6):
        date = datetime.now() + timedelta(days=i)
        dates.append((date.strftime('%Y-%m-%d'), date.strftime('%A')))
    
    timeslots = []
    for date in dates:
        for hours in clinic.working_hours.split(','):
            start_hour, end_hour = map(lambda x: int(x.strip()), hours.split('-'))
            for hour in range(start_hour, end_hour):
                start_time = datetime.strptime(f"{hour}:00", '%H:%M').time()
                end_time = datetime.strptime(f"{hour + 1}:00", '%H:%M').time()
                timeslot = f"{date[0]} {start_time}-{end_time}"
                timeslots.append((timeslot, f"{date[1]} - {start_time}-{end_time}"))

    form.timeslots.choices = timeslots

    if form.validate_on_submit():
        selected_timeslot = form.timeslots.data
        appointment_date, appointment_time = selected_timeslot.split(' ')
        start_time, end_time = appointment_time.split('-')
        appointment = Appointment(
            date=appointment_date,
            time=start_time,
            status=False,
            seen=False,
            clinic_id=clinic.id,
            doctor_id=doctor.id
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('doctor_appointments', doctor_id=doctor.id))

    return render_template('booking.html', form=form, doctor=doctor, dates=dates, clinic=clinic)
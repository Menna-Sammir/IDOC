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
from flask_sqlalchemy import SQLAlchemy
from app.models.models import Specialization, Doctor, Clinic, Governorate, Appointment
from app.views.search import SearchForm
from datetime import datetime, timedelta
from app.views.calnderdoc import AppointmentForm 

admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))

def convert_to_24_hour(time_str):
    return datetime.strptime(time_str, '%I%p').time()

@app.route('/book', methods=['GET', 'POST'])
def doctor_appointments():
    form = AppointmentForm()
    doctor_id = 'doc1'  # يمكنك تعيين ID الدكتور هنا
    doctor = Doctor.query.get_or_404(doctor_id)
    clinic = doctor.clinic
    dates = []

    for i in range(6):
        date = datetime.now() + timedelta(days=i)
        dates.append((date.strftime('%Y-%m-%d'), date.strftime('%A')))

    timeslots_by_date = {}

    for date in dates:
        daily_timeslots = []
        for hours in clinic.working_hours.split(','):
            start_hour, end_hour = map(lambda x: x.strip(), hours.split('-'))
            start_hour_24 = convert_to_24_hour(start_hour)
            end_hour_24 = convert_to_24_hour(end_hour)

            start_hour_int = start_hour_24.hour
            end_hour_int = end_hour_24.hour

            for hour in range(start_hour_int, end_hour_int):
                start_time = datetime.strptime(f"{hour}:00", '%H:%M').time()
                end_time = datetime.strptime(f"{hour + 1}:00", '%H:%M').time()
                timeslot = f"{date[0]} {start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"
                daily_timeslots.append((timeslot, f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"))

        timeslots_by_date[date[0]] = daily_timeslots

    return render_template('booking.html', form=form, doctor=doctor, dates=dates, timeslots_by_date=timeslots_by_date, clinic=clinic)
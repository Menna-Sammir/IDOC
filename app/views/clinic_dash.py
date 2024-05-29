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
from app.models.models import Specialization, Doctor, Clinic, Governorate, Appointment, Patient
from app.views.search import SearchForm
from datetime import datetime, timedelta
from app.views.booking import AppointmentForm 
admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


@app.route('/clinic')
def clinic_details():
    clinic_id = 'cl1'
    clinic = Clinic.query.get_or_404(clinic_id)
    clinic_image_path = "../static/img/clinic/" + clinic.photo
    today = datetime.today().date()
    current_time = datetime.now().time()
    today_appointments = db.session.query(Appointment).filter_by(clinic_id=clinic_id, date=today).count()
    total_appointments = db.session.query(Appointment).filter_by(clinic_id=clinic_id).count()
    today = datetime.today().strftime('%Y-%m-%d')

    working_hours = clinic.working_hours.split('-')
    opening_time = datetime.strptime(working_hours[0], '%I%p').time()
    closing_time = datetime.strptime(working_hours[1], '%I%p').time()
    is_open_today = opening_time <= current_time <= closing_time

    appointments = db.session.query(Appointment, Patient, Doctor).\
        join(Patient, Appointment.patient_id == Patient.id).\
        join(Doctor, Appointment.doctor_id == Doctor.id).\
        filter(Appointment.clinic_id == clinic_id, Appointment.date >= today).all()
    
    patient_image_paths = {}
    for appointment, patient, doctor in appointments:
        patient_image_paths[patient.id] = "../static/img/patient/" + str(patient.photo)

    return render_template('clinic-dashboard.html', clinic=clinic, clinic_image_path=clinic_image_path, today_appointments=today_appointments, total_appointments=total_appointments, is_open_today=is_open_today, today=today, appointments=appointments, patient_image_paths=patient_image_paths)
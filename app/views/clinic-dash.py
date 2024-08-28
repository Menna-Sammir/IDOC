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
from app.models.models import Specialization, Doctor, Clinic, Governorate, Appointment, Patient
from app.views.search import SearchForm
from datetime import datetime, timedelta
from app.views.booking import AppointmentForm 
admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


@app.route('/cliiiiiinic')
def clinic_details():
    clinic_id = 'cl1'
    clinic = Clinic.query.get_or_404(clinic_id)
    today = datetime.today().date()
    
    appointments = db.session.query(Appointment, Patient, Doctor).join(Patient, Appointment.patient_id == Patient.id).join(Doctor, Appointment.doctor_id == Doctor.id).filter(Appointment.clinic_id == clinic_id, Appointment.date >= today).all()
    
    return render_template('clinic-dashboard.html', clinic=clinic, appointments=appointments)
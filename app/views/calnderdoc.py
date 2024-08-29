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
from app.views.booking import AppointmentForm 
from wtforms import StringField,PasswordField, SubmitField, SelectField
from flask_wtf import FlaskForm

admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))

class bookdoc(FlaskForm):
    timeslots = SelectField('Choose a time slot', choices=[])
    submit = SubmitField('Book Appointment')
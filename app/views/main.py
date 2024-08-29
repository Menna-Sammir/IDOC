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



@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    form.specialization.choices = [(s.id, s.specialization_name) for s in Specialization.query.all()]
    form.governorate.choices = [(g.id, g.governorate_name) for g in Governorate.query.all()]

    if form.validate_on_submit():
        specialization_id = form.specialization.data
        governorate_id = form.governorate.data
        doctor_name = form.doctor_name.data
        return redirect(url_for('search_results', specialization_id=specialization_id, governorate_id=governorate_id, doctor_name=doctor_name))
    
    return render_template('index.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def doctor_signup_page():
    form = RegisterDocForm()
    users = (
        User.query.filter(User.doctor_id.isnot(None))
        .with_entities(User.doctor_id)
        .all()
    )
    users = [u[0] for u in users]
    doctors = Doctor.query.filter(not_(Doctor.id.in_(users))).all()
    form.doctor_id.choices = [(doc.id, doc.name) for doc in doctors]
    if request.method == 'POST':
        if form.validate_on_submit():
            user_to_create = User(
                name=form.username.data,
                email=form.email_address.data,
                password_hash=form.password1.data,
                doctor_id=form.doctor_id.data
            )
            role_to_create = Role(role_name='doctor', user=user_to_create)
            db.session.add(user_to_create)
            db.session.add(role_to_create)
            db.session.commit()
            login_user(user_to_create)
            flash(
                f'account created Success! You are logged in as: {user_to_create.name}',
                category='success'
            )
            return redirect(url_for('doctor_dashboard'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
    return render_template('doctor-signup.html', form=form)



@app.route('/register-clinic', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def clinic_signup_page():
    form = RegisterClinicForm()
    users = (
        User.query.filter(User.clinic_id.isnot(None))
        .with_entities(User.clinic_id)
        .all()
    )
    users = [u[0] for u in users]
    clinics = Clinic.query.filter(not_(Clinic.id.in_(users))).all()
    form.clinic_id.choices = [(clinic.id, clinic.name) for clinic in clinics]
    if request.method == 'POST':
        if form.validate_on_submit():
            user_to_create = User(
                name=form.username.data,
                email=form.email_address.data,
                password_hash=form.password1.data,
                clinic_id=form.clinic_id.data
            )
            role_to_create = Role(role_name='clinic', user=user_to_create)
            db.session.add(user_to_create)
            db.session.add(role_to_create)
            db.session.commit()
            login_user(user_to_create)
            flash(
                f'account created Success! You are logged in as: {user_to_create.name}',
                category='success'
            )
            return redirect(url_for('clinic_dashboard'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )

        return render_template('clinic-signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            attempted_user = User.query.filter_by(email=form.email_address.data).first()

            if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
            ):
                login_user(attempted_user)
                identity_changed.send(current_app._get_current_object(), identity=Identity(attempted_user.id))

                flash(
                    f'Success! You are logged in as: {attempted_user.name}',
                    category='success'
                )
                return redirect(url_for('home_page'))
            else:
                flash('user name and password are not match', category='danger')
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    flash('You have been logged out!', category='info')
    return redirect(url_for('home_page'))

@app.errorhandler(403)
def permission_denied(e):
    return 'Permission Denied', 403


@app.route('/doctor-dashboard', methods=['GET', 'POST'])
def doctor_dashboard():
    return render_template('doctor-dashboard.html')


@app.route('/clinic_dashboard', methods=['GET', 'POST'])
def clinic_dashboard():
    return render_template('doctor-dashboard.html')
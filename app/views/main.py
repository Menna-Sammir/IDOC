from app import app, db, principal
from flask import render_template, redirect, url_for, flash, request, current_app
from app.models.models import *
from app.views.forms.auth_form import (
    RegisterDocForm,
    LoginForm,
    RegisterClinicForm,
    AppointmentForm,
    ChangePasswordForm
)
from app.views.forms.search import SearchForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import not_
from flask_principal import (
    Permission,
    RoleNeed,
    Identity,
    AnonymousIdentity,
    identity_loaded,
    identity_changed
)
from flask import Flask, render_template
from datetime import datetime, timedelta
from app.views.booking import AppointmentForm
from datetime import datetime, timedelta
from flask import session


admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    form.specialization.choices = [
        (s.id, s.specialization_name) for s in Specialization.query.all()
    ]
    form.governorate.choices = [
        (g.id, g.governorate_name) for g in Governorate.query.all()
    ]
    if request.method == 'POST':
        if form.validate_on_submit():
            specialization_id = form.specialization.data
            governorate_id = form.governorate.data
            doctor_name = form.doctor_name.data
            session['specialization_id'] = specialization_id
            session['governorate_id'] = governorate_id
            session['doctor_name'] = doctor_name
            return redirect(url_for('search_doctor'))
    if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
    return render_template('index.html', form=form)


@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
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
            user = User.query.filter_by(name=form.username.data).first()
            if not user:
                photo = Doctor.query.filter_by(id=form.doctor_id.data).first().photo
                user_to_create = User(
                    name=form.username.data,
                    email=form.email_address.data,
                    password_hash=form.password1.data,
                    doctor_id=form.doctor_id.data,
                    photo=photo
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
                return redirect(
                    url_for('doctor_dashboard'), current_user=user_to_create.id
                )
            flash(f'this account already exists', category='danger')
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
    return render_template('doctor-signup.html', form=form)


@app.route('/register-clinic', methods=['GET', 'POST'], strict_slashes=False)
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
            user = User.query.filter_by(name=form.username.data).first()
            if not user:
                photo = Clinic.query.filter_by(id=form.clinic_id.data).first().photo
                user_to_create = User(
                    name=form.username.data,
                    email=form.email_address.data,
                    password_hash=form.password1.data,
                    clinic_id=form.clinic_id.data,
                    photo=photo
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
                return redirect(url_for('clinic_dash'), current_user=user_to_create.id)
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
    return render_template('clinic-signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login_page():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            attempted_user = User.query.filter_by(email=form.email_address.data).first()

            if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
            ):
                login_user(attempted_user)
                identity_changed.send(
                    current_app._get_current_object(),
                    identity=Identity(attempted_user.id)
                )

                flash(
                    f'Success! You are logged in as: {attempted_user.name}',
                    category='success'
                )
                # return redirect(url_for('home'))
                session['current_user'] = attempted_user.id
                if attempted_user.roles.role_name == 'Admin':
                    return redirect(url_for('dashboard'))
                elif attempted_user.roles.role_name == 'doctor':
                    return redirect(url_for('doctor_dash'))
                elif attempted_user.roles.role_name == 'clinic':
                    return redirect(url_for('clinic_details'))
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


@app.route('/logout', methods=['GET', 'POST'], strict_slashes=False)
def logout_page():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(), identity=AnonymousIdentity()
    )
    flash('You have been logged out!', category='info')
    return redirect(url_for('home'))
    # return redirect(url_for('login_page'))


@app.route(
    '/change_password',
    methods=['GET', 'POST'],
    strict_slashes=False,
    endpoint='change_password'
)
@login_required
def change_password():
    form = ChangePasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if current_user.check_password_correction(form.current_password.data):
                current_user.password_hash = form.new_password.data
                db.session.commit()
                flash('Your password has been updated!', 'success')
                if current_user.roles.role_name == 'Admin':
                    return redirect(url_for('dashboard'))
                elif current_user.roles.role_name == 'doctor':
                    return redirect(url_for('doctor_dash'))
                elif current_user.roles.role_name == 'clinic':
                    return redirect(url_for('clinic_dash'))
            else:
                flash('Current password is incorrect.', 'danger')
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
    return render_template('change-password.html', form=form)


@app.errorhandler(403)
def permission_denied(e):
    return 'Permission Denied', 403


# @app.route('/doctor-dashboard', methods=['GET', 'POST'])
# def doctor_dashboard():
#     return render_template('doctor-dashboard.html')
#     flash('You not authorized to open this page, please login', category='warning')
#     return redirect(url_for('login_page'))


# @app.route('/clinic_dashboard', methods=['GET', 'POST'], strict_slashes=False)
# def clinic_dashboard():
#     return render_template('doctor-dashboard.html')


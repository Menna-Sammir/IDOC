from app import app, db
from flask import render_template, redirect, url_for, flash, request, current_app
from app.models.models import *
from app.views.forms.auth_form import RegisterDocForm, LoginForm, RegisterClinicForm, ChangePasswordForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import not_
from flask_principal import Permission, RoleNeed, Identity, AnonymousIdentity, identity_changed
from app import socketio



admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


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
                    photo= f"doctors/{photo}"
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
                return redirect(url_for('doctor_dash'))
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
                    photo= f"clinic/{photo}"
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
                return redirect(url_for('clinic_dash'))
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
                if attempted_user.roles.role_name == 'Admin':
                    return redirect(url_for('admin_dash'))
                elif attempted_user.roles.role_name == 'doctor':
                    return redirect(url_for('doctor_dash'))
                elif attempted_user.roles.role_name == 'clinic':
                    return redirect(url_for('clinic_dash'))
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
    print(f"User before logout: {current_user}")
    logout_user()
    print(f"User after logout: {current_user}")
    identity_changed.send(
        current_app._get_current_object(), identity=AnonymousIdentity()
    )
    flash('You have been logged out!', category='info')
    socketio.emit('disconnect request')
    return redirect(url_for('login_page'))


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
                    return redirect(url_for('admin_dash'))
                elif current_user.roles.role_name == 'doctor':
                    return redirect(url_for('doctor_dash'))
                elif current_user.roles.role_name == 'clinic':
                    return redirect(url_for('clinic_dash'))
                return redirect(url_for('home_page'))
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


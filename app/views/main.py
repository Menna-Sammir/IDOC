from app import app, db, socketio
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app,
    session
)
from app.models.models import *
from app.views.forms.auth_form import (
    LoginForm,
    RegisterForm,
    ChangePasswordForm,
    ResetPasswordForm,
    AppointmentForm
)
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import not_
from flask_principal import (
    Permission,
    RoleNeed,
    Identity,
    AnonymousIdentity,
    identity_changed
)
from flask_socketio import disconnect
from datetime import datetime, timedelta
from sqlalchemy import asc


admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def signup_page():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=form.username.data).first()
            if not user:
                user_to_create = User(
                    name=form.username.data,
                    email=form.email_address.data,
                    password_hash=form.password1.data,
                    activated=True
                )
                patient_create = Patient(phone=form.phone.data, users=user_to_create)
                patient_role = Role.query.filter_by(role_name='patient').first_or_404()
                role_to_create = UserRole(role_id=patient_role.id, user=user_to_create)
                db.session.add(user_to_create)
                db.session.add(role_to_create)
                db.session.add(patient_create)
                db.session.commit()
                login_user(user_to_create)
                flash(
                    f'account created Success! You are logged in as: {user_to_create.name}',
                    category='success'
                )
                return redirect(url_for('patient_dashboard'))
            flash(f'this account already exists', category='danger')
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login_page():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            attempted_user = User.query.filter_by(email=form.email_address.data).first()
            if not attempted_user:
                attempted_user = (
                    Doctor.query.filter_by(iDNum=form.email_address.data).first().users
                )
            if attempted_user.activated or not attempted_user.temp_password:
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
                    if attempted_user.user_roles.role.role_name == 'Admin':
                        return redirect(url_for('dashboard'))
                    elif attempted_user.user_roles.role.role_name == 'doctor':
                        return redirect(url_for('doctor_dash'))
                    elif attempted_user.user_roles.role.role_name == 'clinic':
                        return redirect(url_for('clinic_dash'))
                    elif attempted_user.user_roles.role.role_name == 'patient':
                        return redirect(url_for('patient_dashboard'))
                    return redirect(url_for('home_page'))
                else:
                    flash('user name and password are not match', category='danger')
            else:
                flash(f'please check your mail to get password', category='warning')
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
    return render_template('login.html', form=form)


@socketio.on('disconnect request')
def handle_disconnect_request():
    session_id = request.sid
    disconnect(sid=session_id)


@app.route('/logout', methods=['GET', 'POST'], strict_slashes=False)
def logout_page():
    print(f"User before logout: {current_user}")
    logout_user()
    print(f"User after logout: {current_user}")
    identity_changed.send(
        current_app._get_current_object(), identity=AnonymousIdentity()
    )
    flash('You have been logged out!', category='info')
    session.pop('clinic_id', None)
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
                if current_user.user_roles.role.role_name == 'Admin':
                    return redirect(url_for('admin_dash'))
                elif current_user.user_roles.role.role_name == 'doctor':
                    return redirect(url_for('doctor_dash'))
                elif current_user.user_roles.role.role_name == 'clinic':
                    return redirect(url_for('clinic_dash'))
                elif current_user.user_roles.role.role_name == 'patient':
                    return redirect(url_for('patient_dashboard'))
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


@app.route('/reset_password/<email>', methods=['GET', 'POST'])
def reset_password(email):
    user = User.query.filter_by(email=email).first_or_404()
    form = ResetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            temp_password = form.Temp_password.data
            if user.temp_password_correction(attempted_password=temp_password):
                user.password_hash = form.new_password.data
                user.temp_password = None
                user.activated = True
                db.session.commit()
                flash('Your password has been updated!', 'success')
                return redirect(url_for('login_page'))
            else:
                flash('Invalid temporary password.', 'danger')
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
    return render_template('reset_password.html', email=email, form=form)


@app.errorhandler(403)
def permission_denied(e):
    return 'Permission Denied', 403


from app import app, db, socketio
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app,
    session
)
from app.models.models import *
from app.views.forms.auth_form import (
    LoginForm,
    RegisterForm,
    ChangePasswordForm,
    ResetPasswordForm
)
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import not_
from flask_principal import (
    Permission,
    RoleNeed,
    Identity,
    AnonymousIdentity,
    identity_changed
)
from flask_socketio import disconnect
from datetime import datetime, timedelta

admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def signup_page():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=form.username.data).first()
            if not user:
                user_to_create = User(
                    name=form.username.data,
                    email=form.email_address.data,
                    password_hash=form.password1.data,
                    activated=True
                )
                patient_create = Patient(phone=form.phone.data, users=user_to_create)
                patient_role = Role.query.filter_by(role_name='patient').first_or_404()
                role_to_create = UserRole(role_id=patient_role.id, user=user_to_create)
                db.session.add(user_to_create)
                db.session.add(role_to_create)
                db.session.add(patient_create)
                db.session.commit()
                login_user(user_to_create)
                flash(
                    f'account created Success! You are logged in as: {user_to_create.name}',
                    category='success'
                )
                return redirect(url_for('patient_dashboard'))
            flash(f'this account already exists', category='danger')
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login_page():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            attempted_user = User.query.filter_by(email=form.email_address.data).first()
            if not attempted_user:
                attempted_user = (
                    Doctor.query.filter_by(iDNum=form.email_address.data).first().users
                )
            if attempted_user.activated or not attempted_user.temp_password:
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
                    if attempted_user.user_roles.role.role_name == 'Admin':
                        return redirect(url_for('dashboard'))
                    elif attempted_user.user_roles.role.role_name == 'doctor':
                        return redirect(url_for('doctor_dash'))
                    elif attempted_user.user_roles.role.role_name == 'clinic':
                        return redirect(url_for('clinic_dash'))
                    elif attempted_user.user_roles.role.role_name == 'patient':
                        return redirect(url_for('patient_dashboard'))
                    return redirect(url_for('home_page'))
                else:
                    flash('user name and password are not match', category='danger')
            else:
                flash(f'please check your mail to get password', category='warning')
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
    return render_template('login.html', form=form)


@socketio.on('disconnect request')
def handle_disconnect_request():
    session_id = request.sid
    disconnect(sid=session_id)


@app.route('/logout', methods=['GET', 'POST'], strict_slashes=False)
def logout_page():
    print(f"User before logout: {current_user}")
    logout_user()
    print(f"User after logout: {current_user}")
    identity_changed.send(
        current_app._get_current_object(), identity=AnonymousIdentity()
    )
    flash('You have been logged out!', category='info')
    session.pop('clinic_id', None)
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
                if current_user.user_roles.role.role_name == 'Admin':
                    return redirect(url_for('admin_dash'))
                elif current_user.user_roles.role.role_name == 'doctor':
                    return redirect(url_for('doctor_dash'))
                elif current_user.user_roles.role.role_name == 'clinic':
                    return redirect(url_for('clinic_dash'))
                elif current_user.user_roles.role.role_name == 'patient':
                    return redirect(url_for('patient_dashboard'))
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


@app.route('/reset_password/<email>', methods=['GET', 'POST'])
def reset_password(email):
    user = User.query.filter_by(email=email).first_or_404()
    form = ResetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            temp_password = form.Temp_password.data
            if user.temp_password_correction(attempted_password=temp_password):
                user.password_hash = form.new_password.data
                user.temp_password = None
                user.activated = True
                db.session.commit()
                flash('Your password has been updated!', 'success')
                return redirect(url_for('login_page'))
            else:
                flash('Invalid temporary password.', 'danger')
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
    return render_template('reset_password.html', email=email, form=form)


@app.errorhandler(403)
def permission_denied(e):
    return 'Permission Denied', 403


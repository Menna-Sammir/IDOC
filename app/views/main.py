from app import app, db, principal
from flask import render_template, redirect, url_for, flash, request, current_app
from app.models.models import User, Clinic, Doctor, Role,Appointment
from app.views.forms.auth_form import RegisterDocForm, LoginForm, RegisterClinicForm, AppointmentForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import not_
from flask_principal import Permission, RoleNeed, Identity, AnonymousIdentity, identity_loaded, identity_changed
from datetime import datetime, timedelta

admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))



@app.route('/')
@app.route('/home', strict_slashes=False)
def home_page():
    return render_template('index.html')


@app.route('/test')
def test_page():
    return render_template('search.html')

@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
@login_required
@admin_permission.require(http_exception=403)
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
            user = User.query.filter_by(name= form.username.data).first()
            if not user:
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
                return redirect(url_for('doctor_dashboard'), current_user=user_to_create.id)
            flash(
                    f'this account already exists',
                    category='danger'
                )

        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
    return render_template('doctor-signup.html', form=form)


@app.route('/register-clinic', methods=['GET', 'POST'], strict_slashes=False)
@login_required
@admin_permission.require(http_exception=403)
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
            return redirect(url_for('doctor_dashboard'), current_user=user_to_create.id)
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
                identity_changed.send(current_app._get_current_object(), identity=Identity(attempted_user.id))

                flash(
                    f'Success! You are logged in as: {attempted_user.name}',
                    category='success'
                )
                if(attempted_user.roles.role_name == 'Admin'):
                    return redirect(url_for('doctor_dashboard', current_user=attempted_user.id))
                elif(attempted_user.roles.role_name == 'doctor'):
                    return redirect(url_for('doctor_dashboard', current_user=attempted_user.id))
                elif(attempted_user.roles.role_name == 'clinic'):
                    return redirect(url_for('doctor_dashboard', current_user=attempted_user.id))
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
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    flash('You have been logged out!', category='info')
    return redirect(url_for('home_page'))


@app.errorhandler(403)
def permission_denied(e):
    flash('You not authorized to open this page, please login', category='warning')
    return redirect(url_for('login_page'))


@app.route('/doctor-dashboard', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def doctor_dashboard():
    current_user = request.args.get('current_user',None)
    print(current_user)

    return render_template('doctor-dashboard.html')


@app.route('/clinic_dashboard', methods=['GET', 'POST'], strict_slashes=False)
def clinic_dashboard():
    return render_template('doctor-dashboard.html')

@app.route('/booking', methods=['GET', 'POST'], strict_slashes=False)
def doctor_appointments():
    form = AppointmentForm()

    doctor_id = 'doc1'
    doctor = Doctor.query.get_or_404(doctor_id)
    clinic = doctor.clinic
    dates = []
    for i in range(6):
        date = datetime.now() + timedelta(days=i)
        dates.append((date.strftime('%Y-%m-%d'), date.strftime('%A')))
    working_hours = clinic.working_hours.split(',')
    timeslots = []
    for date in dates:
        for hour in working_hours:
            timeslot = f"{date[0]} {hour.strip()}"
            timeslots.append((timeslot, f"{date[1]} - {hour.strip()}"))
    form.timeslots.choices = timeslots
    if form.validate_on_submit():
        selected_timeslot = form.timeslots.data
        appointment = Appointment(
            date=selected_timeslot.split()[0],
            time=selected_timeslot.split()[1],
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
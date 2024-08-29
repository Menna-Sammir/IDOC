from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.models.models import User, Clinic, Doctor, Role
from app.views.auth_form import RegisterDocForm, LoginForm, RegisterClinicForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import not_


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/test')
def test_page():
    return render_template('search.html')


@app.route('/register', methods=['GET', 'POST'])
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
            print(attempted_user)
            if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
            ):
                login_user(attempted_user)
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
    flash('You have been logged out!', category='info')
    return redirect(url_for('home_page'))


@app.route('/doctor-dashboard', methods=['GET', 'POST'])
def doctor_dashboard():
    return render_template('doctor-dashboard.html')


@app.route('/clinic_dashboard', methods=['GET', 'POST'])
def clinic_dashboard():
    return render_template('doctor-dashboard.html')

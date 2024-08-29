from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.models.models import *
from app.views.auth_form import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import not_
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.models.models import Specialization, Doctor, Clinic, Governorate, Appointment
from app.views.search import SearchForm
from datetime import datetime, timedelta
from app.views.booking import AppointmentForm

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
def doctor_signup_page():
    form = RegisterForm()
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
            db.session.add(user_to_create)
            db.session.commit()
            login_user(user_to_create)
            flash(
                f'account created Success! You are logged in as: {user_to_create.name}',
                category='success'
            )
            return redirect(url_for('test_page'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}', category='danger'
                )
    else:
        return render_template('doctor-signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/booking/<string:doctor_id>', methods=['GET', 'POST'])
def doctor_appointments(doctor_id):
    form = AppointmentForm()
    if request.method == 'GET':
        
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
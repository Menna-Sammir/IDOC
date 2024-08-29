from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.models.models import *
from app.views.auth_form import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')



@app.route('/test')
def test_page():
    return render_template('doctor-signup.html')


@app.route('/register', methods=['GET', 'POST'])
def doctor_signup_page():
    form = RegisterForm()
    subquery = User.query.with_entities(User.doctor_id).subquery()
    form.doctor.choices = [
        (doctor.id, doctor.name)
        for doctor in Doctor.query.filter(~Doctor.id.in_(subquery)).all()
    ]

    return render_template('doctor-signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    return render_template('login.html', form=form)

from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.models.models import *
from app.views.auth_form import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import not_
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.models.models import Specialization


@app.route('/')
@app.route('/home')
def home_page():
    specializations = Specialization.query.all()
    specializations_valu = [(spe.id, spe.specialization_name) for spe in specializations]
    print(specializations_valu)
    return render_template('index.html', specializations=specializations_valu)


@app.route('/test')
def test_page():
    return render_template('search.html')


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

from app import app
from flask import render_template, redirect, url_for, flash, request
from app.models.models import Specialization, User, Doctor,  Patient, Appointment, Clinic, Message,  Governorate, Role



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/test')
def test_page():
    return render_template('doctor-signup.html')


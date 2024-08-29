from app import app
from flask import render_template, redirect, url_for, flash, request
from app.models.models import Specialization, User, Doctor,  Patient, Appointment, Clinic, Message,  Governorate, Role



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

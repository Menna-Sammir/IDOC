from app import app
from flask import render_template, redirect, url_for, flash, request
from app.models.models import Specialization, User, Doctor,  Patient, Appointment, Clinic, Message,  Governorate, Role



@app.route('/')
@app.route('/search_doctor')
def search_doctor():
    
    return render_template('search.html')





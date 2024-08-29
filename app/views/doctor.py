from app import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from datetime import datetime
from sqlalchemy import func, or_
from app.models.models import Specialization, User, Doctor,  Patient, Appointment, Clinic, Message,  Governorate, Role


@app.route('/search_doctor', methods=['GET', 'POST'])
def search_doctor():
    specialization_name = request.args.getlist('specialization_name')
    doctor_name = request.args.get('doctor_name')
    clinic_address = request.args.get('clinic_address')
    date = request.args.get('date')
    max_appointments = 5

    query = db.session.query(Doctor, Specialization, Clinic, Governorate) \
        .join(Specialization, Doctor.specialization_id == Specialization.id) \
        .join(Clinic, Doctor.clinic_id == Clinic.id) \
        .join(Governorate, Clinic.governorate_id == Governorate.id)

    if specialization_name:
        query = query.filter(Doctor.specialization_id.in_(specialization_name))
    if doctor_name:
        query = query.filter(Doctor.name.like(f'%{doctor_name}%'))
    if clinic_address:
        query = query.filter(Clinic.address.like(f'%{clinic_address}%'))
    if date:
        search_date = datetime.strptime(date, '%Y-%m-%d').date()
        # Add your appointment-related filter here

    doctors = query.all()
    specializations = Specialization.query.all()
    governorates = Governorate.query.all()

    return render_template('search.html', doctors=doctors, specializations=specializations, governorates=governorates)

    
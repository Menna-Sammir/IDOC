from app import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from datetime import datetime
from sqlalchemy import func, select
from flask import session
from app.models.models import Specialization, User, Doctor,  Patient, Appointment, Clinic, Message,  Governorate, Role


@app.route('/search_doctor', methods=['GET', 'POST'])
def search_doctor():
    query = db.session.query(Doctor, Specialization, Clinic, Governorate) \
        .join(Specialization, Doctor.specialization_id == Specialization.id) \
        .join(Clinic, Doctor.clinic_id == Clinic.id) \
        .join(Governorate, Clinic.governorate_id == Governorate.id)

    specializations = Specialization.query.all()
    governorates = Governorate.query.all()

    if request.method == 'POST':
        specialization_ids = request.form.getlist('select_specialization')
        date = request.form.get('date')
        
        if specialization_ids:
            query = query.filter(Doctor.specialization_id.in_(specialization_ids))
        
        if date:
            search_date = datetime.strptime(date, '%d/%m/%Y').date()
            subquery = db.session.query(Appointment.doctor_id).filter(
                func.date(Appointment.date) == search_date).group_by(
                Appointment.doctor_id).having(func.count(Appointment.id) < 5).subquery()
            query = query.filter(Doctor.id.in_(select(subquery)))

    doctors = query.all()
    return render_template('search.html', doctors=doctors, specializations=specializations, governorates=governorates)


@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        session['doctor_id'] = doctor_id
        return redirect('booking.html')

@app.route('/doctor_dashboard')
def doctor_dashboard():
    return render_template('doctor-dashboard.html')

    # query = db.session.query(Appointment, Patient, Clinic, Governorate) \
    #     .join(Patient, Appointment.patient_id == Patient.id) \
    #     .join(Clinic, Appointment.clinic_id == Clinic.id) \
    #     .join(Governorate, Clinic.governorate_id == Governorate.id)
        
    # Patient = Patient.query.all()
    # Clinic = Clinic.query.all()
    # Governorate = Governorate.query.all()
    # Appointment = Appointment.query.all()








from app import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from datetime import datetime
from sqlalchemy import func, select, and_
from sqlalchemy.orm import joinedload
from flask_paginate import Pagination, get_page_args
from flask_login import login_required, current_user
from flask import session
from datetime import date
from app.models.models import Specialization, User, Doctor,  Patient, Appointment, Clinic, Message,  Governorate, Role
from flask_principal import Permission, RoleNeed, Identity, AnonymousIdentity, identity_loaded, identity_changed

admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


# doctor search page
@app.route('/search_doctor', methods=['GET', 'POST'])
def search_doctor():
    page = request.args.get('page', 1, type=int)
    per_page = 10 
    
    query = db.session.query(Doctor, Specialization, Clinic, Governorate) \
        .join(Specialization, Doctor.specialization_id == Specialization.id) \
        .join(Clinic, Doctor.clinic_id == Clinic.id) \
        .join(Governorate, Clinic.governorate_id == Governorate.id)

    specializations = Specialization.query.all()
    governorates = Governorate.query.all()

    selected_specializations = []
    selected_date = None

    if request.method == 'POST':
        selected_specializations = request.form.getlist('select_specialization')
        selected_date = request.form.get('date')

        if selected_specializations:
            query = query.filter(Doctor.specialization_id.in_(selected_specializations))
        
        if selected_date:
            search_date = datetime.strptime(selected_date, '%d/%m/%Y').date()
            subquery = db.session.query(Doctor.id).outerjoin(Appointment, and_(
                Doctor.id == Appointment.doctor_id,
                func.date(Appointment.date) == search_date
            )).filter(Appointment.id == None)

            query = query.filter(Doctor.id.in_(subquery))
            print(f"Query: {query}")
    pagination = query.paginate(page, per_page, False)
    doctors = pagination.items
    print(f"Doctors: {doctors}")
    print(f"Generated SQL Query: {query}")
    return render_template('search.html', doctors=doctors, 
                           specializations=specializations, governorates=governorates,
                           selected_specializations=selected_specializations,
                           selected_date=selected_date,
                           pagination=pagination)
    

# doctor search page >>> book appointment
@app.route('/booking', methods=['POST'])
def book_appointment():
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')

        session['doctor_id'] = doctor_id
        return redirect(url_for('doctor_appointments'))


# @app.route('/book_appointment_form')
# def book_appointment_form():
#     doctor_id = session.get('doctor_id', None)
#     if doctor_id:
#         return f'Booking appointment with doctor_id={doctor_id}'
#     else:
#         return 'No doctor_id found in session.'


# doctor dashboard page >>> view appointments today
@app.route('/doctor_dashboard', methods=['GET', 'POST'])
@login_required
@doctor_permission.require(http_exception=403)
def doctor_dash():
    user_id = request.args.get('current_user', None)
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return "User not found", 404

    if not hasattr(user, 'doctor_id'):
        return "User is not a doctor", 403

    doctor_id = user.doctor_id
    doctor = Doctor.query.filter_by(id=doctor_id).first()

    if doctor is None:
        return "Doctor not found", 404

    today = date.today()

    appointments = db.session.query(Appointment, Doctor.name, Specialization.specialization_name, Patient.name, Patient.phone)\
        .join(Doctor, Doctor.id == Appointment.doctor_id)\
        .join(Specialization, Specialization.id == Doctor.specialization_id)\
        .join(Patient, Patient.id == Appointment.patient_id)\
        .filter(Appointment.doctor_id == doctor_id, Appointment.date == today, Appointment.seen == False).all()

    specialization = Specialization.query.filter(Specialization.id == doctor.specialization_id).first()
    
    appointments_list = []
    for appointment, doctor_name, specialization_name, patient_name, patient_phone in appointments:
        appointments_list.append({
            'appointment_id': appointment.id,
            'appointment_time': appointment.time,
            'appointment_date': appointment.date,
            'patient_name': patient_name,
            'doctor_name': doctor_name,
            'photo': doctor.photo,
            'patient_phone': patient_phone,
            'specialization_name': specialization_name,
            'status': appointment.status,
            'seen': appointment.seen
        })
        
    patient_count = len(appointments_list)
    
    if request.method == 'POST':
        if 'logout' in request.form:
            return redirect(url_for('logout'))
        
        if 'seen' in request.form:
            appointment_id = request.form.get('appointment_id')
            appointment = Appointment.query.get(appointment_id)
            if appointment:
                appointment.seen = True
                db.session.commit()
            return redirect(url_for('doctor_dash', current_user=user_id))

    return render_template('doctor-dashboard.html', current_user=user, doctor=doctor, appointments=appointments_list, specialization=specialization, patient_count=patient_count, today=today)


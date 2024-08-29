from app import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from datetime import datetime
from sqlalchemy import func, select, and_
from sqlalchemy.orm import joinedload
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
            subquery = db.session.query(Doctor.id).outerjoin(Appointment, and_(
            Doctor.id == Appointment.doctor_id,
            func.date(Appointment.date) == search_date
            )).filter(Appointment.id == None)

            query = query.filter(Doctor.id.in_(subquery))
            
    doctors = query.all()
    return render_template('search.html', doctors=doctors, specializations=specializations, governorates=governorates)

# doctor search page >>> book appointment
@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        session['doctor_id'] = doctor_id
        return redirect('booking.html')


# doctor dashboard page >>> view appointments today
@app.route('/doctor_dashboard', methods=['GET', 'POST'])
@login_required
def doctor_dash():
    user_id = request.args.get('current_user', None)
    
    user = User.query.filter_by(id=user_id).first()

    doctor_id = user.doctor_id

    doctor = Doctor.query.filter_by(id=doctor_id).first()

    today = date.today()
    print("Today's date:", today)
    print("User ID:", user_id)
    print("Doctor ID:", doctor_id)
    print("Doctor:", doctor)

    appointments = db.session.query(Appointment, Doctor.name, Specialization.specialization_name, Patient.name)\
        .join(Doctor, Doctor.id == Appointment.doctor_id)\
        .join(Specialization, Specialization.id == Doctor.specialization_id)\
        .join(Patient, Patient.id == Appointment.patient_id)\
        .filter(Appointment.doctor_id == doctor_id, Appointment.date == today).all()
        
    specialization = Specialization.query.filter(Specialization.id == doctor.specialization_id).first()
    
    
    appointments_list = []
    for appointment, doctor_name, specialization_name, patient_name in appointments:
        appointments_list.append({
            'appointment_id': appointment.id,
            'appointment_time': appointment.time,
            'appointment_date': appointment.date,
            'patient_name': patient_name,
            'doctor_name': doctor_name,
            'specialization_name': specialization_name,
            'status': appointment.status,
            'seen': appointment.seen
        })
        
    if request.method == 'POST':
        return redirect(url_for('logout'))

    return render_template('doctor-dashboard.html', current_user=user_id, doctor=doctor, appointments=appointments_list, specialization=specialization)



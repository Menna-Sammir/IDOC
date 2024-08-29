from app import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from datetime import datetime
from sqlalchemy import func, select
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
        
        print("Specialization IDs:", specialization_ids)
        print("Date:", date)

        if specialization_ids:
            query = query.filter(Doctor.specialization_id.in_(specialization_ids))
        
        if date:
            search_date = datetime.strptime(date, '%d/%m/%Y').date()
            subquery = db.session.query(Appointment.doctor_id).filter(
                func.date(Appointment.date) == search_date).group_by(
                Appointment.doctor_id).having(func.count(Appointment.id) < 5).subquery()
            query = query.filter(Doctor.id.in_(subquery))

    doctors = query.all()
    print("Doctors:", doctors)  # Debug statement to check the query results
    return render_template('search.html', doctors=doctors, specializations=specializations, governorates=governorates)


# @app.route('/search_doctor', methods=['GET', 'POST'])
# def search_doctor():
#     specialization_name = request.args.getlist('specialization_name')
#     doctor_name = request.args.get('doctor_name')
#     clinic_address = request.args.get('clinic_address')
#     date = request.args.get('date')
#     max_appointments = 5

#     query = db.session.query(Doctor, Specialization, Clinic, Governorate) \
#         .join(Specialization, Doctor.specialization_id == Specialization.id) \
#         .join(Clinic, Doctor.clinic_id == Clinic.id) \
#         .join(Governorate, Clinic.governorate_id == Governorate.id)

#     if specialization_name:
#         query = query.filter(Doctor.specialization_id.in_(specialization_name))
#     if doctor_name:
#         query = query.filter(Doctor.name.like(f'%{doctor_name}%'))
#     if clinic_address:
#         query = query.filter(Clinic.address.like(f'%{clinic_address}%'))
#     if date:
#         search_date = datetime.strptime(date, '%Y-%m-%d').date()
#         query = query.filter(~Doctor.appointments.any(func.date(Appointment.date) == search_date))

#     doctors = query.all()
#     specializations = Specialization.query.all()
#     governorates = Governorate.query.all()
    
#     if request.method == 'POST':
#         specialization_id = request.get('select_specialization')
#         date = request.get('date')
        
#         if specialization_id:
#             query = query.filter(Doctor.specialization_id == specialization_id)
#         if date:
#             pass
#         query = db.session.query(Doctor, Clinic, Governorate).join(Clinic).join(Governorate)
        
#     return render_template('search.html', doctors=doctors, specializations=specializations, governorates=governorates)

    
        
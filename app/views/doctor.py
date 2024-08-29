from app import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from datetime import datetime
from sqlalchemy import func, or_
from app.models.models import Specialization, User, Doctor,  Patient, Appointment, Clinic, Message,  Governorate, Role


@app.route('/search_doctor', methods=['GET', 'POST'])
def search_doctor():
    if request.method == 'GET':

        query = db.session.query(Doctor, Specialization, Clinic, Governorate) \
            .join(Specialization, Doctor.specialization_id == Specialization.id) \
            .join(Clinic, Doctor.clinic_id == Clinic.id) \
            .join(Governorate, Clinic.governorate_id == Governorate.id)

        doctors = query.all()
        specializations = Specialization.query.all()
        governorates = Governorate.query.all()

        return render_template('search.html', doctors=doctors, specializations=specializations, governorates=governorates)

    elif request.method == 'POST':
        specialization_id = request.form.get('select_specialization')
        date = request.form.get('date')


        query = db.session.query(Doctor, Clinic, Governorate).join(Clinic).join(Governorate)
        if specialization_id:
            query = query.filter(Doctor.specialization_id == specialization_id)
        if date:

            pass

        filtered_doctors = query.all()

        return jsonify(doctors=[{
            'name': doctor.name,
            'clinic_address': clinic.address,
            'governorate_name': governorate.name,
            'specialization_name': doctor.specialization.name,
            'price': doctor.price 
        } for doctor, clinic, governorate in filtered_doctors])


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

    
        
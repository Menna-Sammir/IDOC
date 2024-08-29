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
from app.views.forms.auth_form import AppointmentForm

admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


# doctor search page
@app.route('/search_doctor', methods=['GET', 'POST'])
def search_doctor():
    
    specialization_id = session.get('specialization_id', None)
    governorate_id = session.get('governorate_id', None)
    doctor_name = session.get('doctor_name', None)
    
 
    page = request.args.get('page', 1, type=int)
    per_page = 10
    per_page = 10

    form = AppointmentForm()
    
    query = db.session.query(Doctor, Specialization, Clinic, Governorate) \
        .join(Specialization, Doctor.specialization_id == Specialization.id) \
        .join(Clinic, Doctor.clinic_id == Clinic.id) \
        .join(Governorate, Clinic.governorate_id == Governorate.id)

   
    if specialization_id:
        query = query.filter(Doctor.specialization_id == specialization_id)
    if governorate_id:
        query = query.filter(Clinic.governorate_id == governorate_id)
    if doctor_name:
        query = query.filter(Doctor.name.ilike(f'%{doctor_name}%'))

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
        
        if request.form.get('action') == 'book_appointment':
            doctor_id = request.form.get('doctor_id')
            session['doctor_id'] = doctor_id
            print(f"Doctor ID: {doctor_id}")
            return redirect(url_for('book'))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    doctors = pagination.items


    print(f"Doctors: {doctors}")
    print(f"Generated SQL Query: {query}")

    return render_template('search.html', doctors=doctors,
                           specializations=specializations, governorates=governorates,
                           selected_specializations=selected_specializations,
                           selected_date=selected_date,
                           pagination=pagination,
                           form=form)
    

# # doctor search page >>> book appointment
# @app.route('/search_doctor', methods=['GET', 'POST'])
# def search_doctor():
#     if request.method == 'POST':



# doctor dashboard page >>> view appointments today
@app.route('/doctor_dashboard', methods=['GET', 'POST'])
# @login_required
# @doctor_permission.require(http_exception=403)
def doctor_dash():
    user_id = session.get('current_user')
    user = User.query.filter_by(id=user_id).first()
    print("User:", user)

    if user is None:
        return "User not found", 404

    if not hasattr(user, 'doctor_id'):
        return "User is not a doctor", 403

    doctor = Doctor.query.filter_by(id=user.doctor_id).first()

    if doctor is None:
        return "Doctor not found", 404
    form = AppointmentForm()
   
    appointments = Appointment.query.filter_by(date=date.today(), seen=False)
    monthAppointments = Appointment.query.filter(func.extract('month', Appointment.date) == datetime.now().month).count()
    patient_count = appointments.count()

    if request.method == 'POST':
        if 'seen' in request.form:
            appointment_id = request.form.get('appointment_id')
            appointment = Appointment.query.get(appointment_id)
            if appointment:
                appointment.seen = True
                db.session.commit()
                flash('Appointment marked as seen', category='success')
                return redirect(url_for('doctor_dash'))

    return render_template('doctor-dashboard.html',
                           doctor=doctor,
                           appointments=appointments.all(),
                           patient_count=patient_count,
                           monthAppointments=monthAppointments,
                           form=form)


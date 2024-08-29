from app import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from datetime import datetime
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from flask_login import login_required, current_user
from flask import session
from datetime import date
from app.models.models import Specialization, User, Doctor,  Patient, Appointment, Clinic, Message,  Governorate, Role
from flask_principal import Permission, RoleNeed, Identity, AnonymousIdentity, identity_loaded, identity_changed

admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


# admin dashboard page >>> view appointments today
@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dash():
    user_id = request.args.get('current_user', None)
    user = User.query.filter_by(id=user_id).first()
    
    doctors = db.session.query(Doctor).options(
        joinedload(Doctor.specialization),
        joinedload(Doctor.clinic)
    ).all()

    doctor_details = []
    clinic_details = set()
    for doctor in doctors:
        appointment_count = db.session.query(func.count(Appointment.id)).filter(Appointment.doctor_id == doctor.id).scalar() or 0
        total_earnings = appointment_count * (doctor.price or 0)

        details = {
            'doctor_name': doctor.name,
            'specialization': doctor.specialization.specialization_name,
            'photo': doctor.photo,
            'price': doctor.price,
            'clinic_name': doctor.clinic.name,
            'clinic_phone': doctor.clinic.phone,
            'clinic_address': doctor.clinic.address,
            'total_earnings': total_earnings
        }
        doctor_details.append(details)

        clinic_info = {
            'clinic_name': doctor.clinic.name,
            'clinic_phone': doctor.clinic.phone,
            'clinic_address': doctor.clinic.address
        }
        clinic_details.add(frozenset(clinic_info.items()))

    clinic_details = [dict(clinic) for clinic in clinic_details]

    doctor_count = db.session.query(Doctor).count()
    clinic_count = db.session.query(Clinic).count()

    if request.method == 'POST':
        return redirect(url_for('logout'))
    
    return render_template('admin-dashboard.html', 
                           current_user=user,
                           doctor_details=doctor_details,
                           clinic_details=clinic_details, 
                           doctor_count=doctor_count,
                           clinic_count=clinic_count)



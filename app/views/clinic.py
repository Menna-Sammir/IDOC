from app import app, db
from flask import render_template
from app.models.models import *
from flask_principal import Permission, RoleNeed
from flask_login import login_required, current_user

admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


@app.route('/clinic_dashboard', methods=['GET'], strict_slashes=False)
@login_required
@clinic_permission.require(http_exception=403)
def clinic_dash():
    user_id = current_user.id
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return 'User not found', 404
    if not hasattr(user, 'clinic_id'):
        return 'User is not a clinic', 403
    clinic = Clinic.query.get_or_404(user.clinic_id)
    today = datetime.today().date()
    current_time = datetime.now().time()
    today_appointments = db.session.query(Appointment).filter_by(clinic_id=user.clinic_id, date=today).count()
    total_appointments = db.session.query(Appointment).filter_by(clinic_id=user.clinic_id).count()
    today = datetime.today().strftime('%Y-%m-%d')

    working_hours = clinic.working_hours.split('-')
    opening_time = datetime.strptime(working_hours[0], '%I%p').time()
    closing_time = datetime.strptime(working_hours[1], '%I%p').time()
    is_open_today = opening_time <= current_time <= closing_time

    appointments = db.session.query(Appointment, Patient, Doctor).\
        join(Patient, Appointment.patient_id == Patient.id).\
        join(Doctor, Appointment.doctor_id == Doctor.id).\
        filter(Appointment.clinic_id == user.clinic_id, Appointment.date >= today).all()

    return render_template('clinic-dashboard.html', clinic=clinic, today_appointments=today_appointments, total_appointments=total_appointments, is_open_today=is_open_today, appointments=appointments)
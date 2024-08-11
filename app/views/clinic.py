from app import app, db
from flask import render_template, redirect, url_for
from app.models.models import *
from flask_principal import Permission, RoleNeed
from flask_login import login_required, current_user
from app import translate
from datetime import datetime
from flask import jsonify, request
from sqlalchemy.orm import joinedload



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
        return translate('User not found'), 404
    if not hasattr(user, 'clinic_id'):
        return translate('User is not a clinic'), 403
    clinic = Clinic.query.get_or_404(user.clinic_id)
    today = datetime.today().date()
    current_time = datetime.now().time()
    today_appointments = (
        db.session.query(Appointment)
        .filter_by(clinic_id=user.clinic_id, date=today)
        .count()
    )
    total_appointments = (
        db.session.query(Appointment).filter_by(clinic_id=user.clinic_id).count()
    )
    today = datetime.today().strftime('%Y-%m-%d')

    # working_hours = clinic.working_hours.split('-')
    # opening_time = datetime.strptime(working_hours[0].strip().upper(), '%I:%M %p').time()
    # closing_time = datetime.strptime(working_hours[1].strip().upper(), '%I:%M %p').time()
    # is_open_today = opening_time <= current_time <= closing_time

    appointments = (
        db.session.query(Appointment, Patient, Doctor)
        .join(Patient, Appointment.patient_id == Patient.id)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .filter(Appointment.clinic_id == user.clinic_id, Appointment.date >= today)
        .all()
    )
    return render_template(
        'clinic-dashboard.html',
        clinic=clinic,
        today_appointments=today_appointments,
        total_appointments=total_appointments,
        appointments=appointments
    )


@app.route('/calender', methods=['GET'], strict_slashes=False)
@login_required
@clinic_permission.require(http_exception=403)
def clinic_calender():
    user_id = current_user.id
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return translate('User not found'), 404
    if not hasattr(user, 'clinic_id'):
        return translate('User is not a clinic'), 403
    clinic = Clinic.query.get_or_404(user.clinic_id)
    current_time = datetime.now().time()

    # working_hours = clinic.working_hours.split('-')
    # opening_time = datetime.strptime(working_hours[0].strip().upper(), '%I:%M %p').time()
    # closing_time = datetime.strptime(working_hours[1].strip().upper(), '%I:%M %p').time()
    # is_open_today = opening_time <= current_time <= closing_time

    return render_template(
        'clinicCalender.html'
    )


@app.route('/getcaldata', methods=['GET'], strict_slashes=False)
def clinic_cal():
    user_id = current_user.id
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    if not hasattr(user, 'clinic_id'):
        return jsonify({'error': 'User is not a clinic'}), 403
    appointments = (
        db.session.query(Appointment, Patient, Doctor)
        .join(Patient, Appointment.patient_id == Patient.id)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .filter(Appointment.clinic_id == user.clinic_id, Appointment.seen == False)
        .all()
    )
    appointment_events = [
        {
            'doctor': f'{" ".join(appointment.Doctor.name.split()[:2])}',
            'title': f'{" ".join(appointment.Doctor.name.split()[:2])}',
            'patient': f'{" ".join(appointment.Patient.name.split()[:2])}',
            'start': f'{appointment.Appointment.date}T{appointment.Appointment.time}',
            'end': f'{appointment.Appointment.date}T{appointment.Appointment.time}',
            'img': f'../static/images/doctors/{appointment.Doctor.photo}',
            'cost': f'{appointment.Doctor.price}'
        }
        for appointment in appointments
    ]
    return jsonify({'appointment_events': appointment_events})



@app.route('/clear', methods=['GET', 'POST', 'PUT'], strict_slashes=False)
@login_required
@clinic_permission.require(http_exception=403)
def clear_noti():
    clinic_id = current_user.clinic.id
    if clinic_id is None:
        return translate('User not found'), 404
    rows_changed = Notification.query.filter_by(clinic_id=clinic_id).update(dict(isRead=True))
    db.session.commit()
    return redirect(url_for('clinic_calender'))


@app.route('/view_all', methods=['GET'], strict_slashes=False)
def view_notifi():
    current_time = datetime.now()
    if current_user.is_authenticated and hasattr(current_user, 'clinic_id'):
        notifications = (
            db.session.query(Notification)
            .join(Appointment)
            .join(Doctor, Appointment.doctor_id == Doctor.id)
            .join(Patient, Appointment.patient_id == Patient.id)
            .filter(Notification.clinic_id == current_user.clinic_id)
            .options(
                joinedload(Notification.appointment).joinedload(Appointment.doctor),
                joinedload(Notification.appointment).joinedload(Appointment.patient)
            )
            .all()
        )

        processed_notifications = [
            {
                'doctor': n.appointment.doctor.name if n.appointment and n.appointment.doctor else 'Unknown',
                'patient': n.appointment.patient.name if n.appointment and n.appointment.patient else 'Unknown',
                'body': n.noteBody,
                'isRead': n.isRead,
                'time': n.time.strftime('%H:%M %p'),
                'date': n.date.strftime('%d %B'),
                'photo': n.appointment.doctor.photo if n.appointment and n.appointment.doctor else None,
                'formatted_time': calculate_time_ago(current_time, n.notDate)
            }
            for n in notifications[:10]
        ]
        g.notifications = processed_notifications
        g.notification_count = len(
            db.session.query(Notification).filter(
                Notification.clinic_id == current_user.clinic_id,
                Notification.isRead == False
            ).all()
        ) or 0

    return render_template('view_notification.html', notifications=g.get('notifications', []))

@app.route('/delete_notification', methods=['POST'])
@login_required
def delete_notification():
    data = request.get_json()
    notification_id = data.get('id')
    if not notification_id:
        return jsonify({'message': 'No notification ID provided'}), 400

    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'message': 'Notification not found'}), 404

    if notification.clinic_id != current_user.clinic_id:
        return jsonify({'message': 'You are not authorized to delete this notification'}), 403

    db.session.delete(notification)
    db.session.commit()
    return jsonify({'message': 'Notification deleted successfully'}), 200

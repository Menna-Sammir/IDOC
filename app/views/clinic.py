<<<<<<< HEAD
<<<<<<< HEAD
from app import app, db
from flask import render_template, redirect, url_for
from app.models.models import *
from flask_principal import Permission, RoleNeed
from flask_login import login_required, current_user
from app import translate
from datetime import datetime
from flask import jsonify, request
from sqlalchemy.orm import joinedload
from flask_socketio import emit


admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))

@app.route('/clinic_dashboard', methods=['GET'], strict_slashes=False)
@login_required
@clinic_permission.require(http_exception=403)
def clinic_dash():
    clinic = Clinic.query.filter_by(user_id=current_user.id).first()
    if clinic is None:
        return translate('User is not a clinic'), 403
    today = datetime.today().date()
    current_time = datetime.now().time()
    today_appointments = (
        db.session.query(Appointment)
        .filter_by(clinic_id=clinic.id, date=today)
        .count()
    )
    total_appointments = (
        db.session.query(Appointment).filter_by(clinic_id=clinic.id).count()
    )
    today = datetime.today().strftime('%Y-%m-%d')

    # Removed working_hours logic
    is_open_today = None  # Or any other logic if applicable

    appointments = (
        db.session.query(Appointment, Patient, Doctor)
        .join(Patient, Appointment.patient_id == Patient.id)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .filter(Appointment.clinic_id == clinic.id, Appointment.date >= today)
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
    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        return translate('User not found'), 404
    clinic = Clinic.query.filter_by(user_id = current_user.id)
    if clinic is None:
        return translate('User is not a clinic'), 403
    current_time = datetime.now().time()
    # Removed working_hours logic
    is_open_today = None  # Or any other logic if applicable

    return render_template(
        'clinicCalender.html',
        working_hours=None,  # This will be None or you may adjust based on your needs
        is_open_today=is_open_today
    )

@app.route('/getcaldata', methods=['GET'], strict_slashes=False)
def clinic_cal():
    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        return translate('User not found'), 404
    clinic = Clinic.query.filter_by(user_id = current_user.id).first()
    if clinic is None:
        return translate('User is not a clinic'), 403
    appointments = (
        db.session.query(Appointment, Patient, Doctor)
        .join(Patient, Appointment.patient_id == Patient.id)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .filter(Appointment.clinic_id == clinic.id, Appointment.seen == False)
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


### view all notifications page ###
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
                'id': n.id,
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


@app.route('/mark_as_read', methods=['POST'])
@login_required
def mark_as_read():
    notification_id = request.form.get('notification_id')
    if not notification_id:
        return jsonify({'message': 'Notification ID is missing'}), 400

    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'message': 'Notification not found'}), 404

    notification.isRead = True
    db.session.commit()


    return jsonify({'message': 'Notification marked as read'})


@app.route('/delete_notification', methods=['POST'])
@login_required
def delete_notification():
    notification_id = request.form.get('notification_id')
    if not notification_id:
        return jsonify({'message': 'Notification ID is missing'}), 400

    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'message': 'Notification not found'}), 404

    db.session.delete(notification)
    db.session.commit()

    return jsonify({'message': 'Notification deleted'})
=======
=======
>>>>>>> b1ada92490b7c46372fbf52fc152dd4c8744177f
from app import app, db
from flask import render_template, redirect, url_for
from app.models.models import *
from flask_principal import Permission, RoleNeed
from flask_login import login_required, current_user
from app import translate
from datetime import datetime
from flask import jsonify, request
from sqlalchemy.orm import joinedload
from flask_socketio import emit


admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))

@app.route('/clinic_dashboard', methods=['GET'], strict_slashes=False)
@login_required
@clinic_permission.require(http_exception=403)
def clinic_dash():
    clinic = Clinic.query.filter_by(user_id=current_user.id).first()
    if clinic is None:
        return translate('User is not a clinic'), 403
    today = datetime.today().date()
    current_time = datetime.now().time()
    today_appointments = (
        db.session.query(Appointment)
        .filter_by(clinic_id=clinic.id, date=today)
        .count()
    )
    total_appointments = (
        db.session.query(Appointment).filter_by(clinic_id=clinic.id).count()
    )
    today = datetime.today().strftime('%Y-%m-%d')

    # Removed working_hours logic
    is_open_today = None  # Or any other logic if applicable

    appointments = (
        db.session.query(Appointment, Patient, Doctor)
        .join(Patient, Appointment.patient_id == Patient.id)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .filter(Appointment.clinic_id == clinic.id, Appointment.date >= today)
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
    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        return translate('User not found'), 404
    clinic = Clinic.query.filter_by(user_id = current_user.id)
    if clinic is None:
        return translate('User is not a clinic'), 403
    current_time = datetime.now().time()
    # Removed working_hours logic
    is_open_today = None  # Or any other logic if applicable

    return render_template(
        'clinicCalender.html',
        working_hours=None,  # This will be None or you may adjust based on your needs
        is_open_today=is_open_today
    )

@app.route('/getcaldata', methods=['GET'], strict_slashes=False)
def clinic_cal():
    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        return translate('User not found'), 404
    clinic = Clinic.query.filter_by(user_id = current_user.id).first()
    if clinic is None:
        return translate('User is not a clinic'), 403
    appointments = (
        db.session.query(Appointment, Patient, Doctor)
        .join(Patient, Appointment.patient_id == Patient.id)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .filter(Appointment.clinic_id == clinic.id, Appointment.seen == False)
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


### view all notifications page ###
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
                'id': n.id,
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


@app.route('/mark_as_read', methods=['POST'])
@login_required
def mark_as_read():
    notification_id = request.form.get('notification_id')
    if not notification_id:
        return jsonify({'message': 'Notification ID is missing'}), 400

    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'message': 'Notification not found'}), 404

    notification.isRead = True
    db.session.commit()


    return jsonify({'message': 'Notification marked as read'})


@app.route('/delete_notification', methods=['POST'])
@login_required
def delete_notification():
    notification_id = request.form.get('notification_id')
    if not notification_id:
        return jsonify({'message': 'Notification ID is missing'}), 400

    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'message': 'Notification not found'}), 404

    db.session.delete(notification)
    db.session.commit()

    return jsonify({'message': 'Notification deleted'})
<<<<<<< HEAD
>>>>>>> b1ada92490b7c46372fbf52fc152dd4c8744177f
=======
>>>>>>> b1ada92490b7c46372fbf52fc152dd4c8744177f

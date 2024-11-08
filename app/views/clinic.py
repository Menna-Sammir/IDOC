from app import app, db
from flask import render_template, redirect, url_for, flash
from app.models.models import *
from flask_principal import Permission, RoleNeed
from flask_login import login_required, current_user
from app import translate
from datetime import datetime
from flask import jsonify, request
from sqlalchemy.orm import joinedload
from flask_socketio import emit
from app.views.forms.auth_form import EditUserForm
from app.views.forms.addClinic_form import EditClinicForm
import os
from werkzeug.utils import secure_filename
import uuid
import json


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
        db.session.query(Appointment).filter_by(clinic_id=clinic.id, date=today).count()
    )
    total_appointments = (
        db.session.query(Appointment).filter_by(clinic_id=clinic.id).count()
    )
    today = datetime.today().strftime('%Y-%m-%d')

    today_appointments_count = Appointment.query.filter_by(clinic_id=clinic.id, date=today).count()

    today_appointments = (
        db.session.query(Appointment, Patient, Doctor)
        .join(Patient, Appointment.patient_id == Patient.id)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .filter(Appointment.clinic_id == clinic.id, Appointment.date == today)
        .all()
    )

    upcoming_appointments = (
        db.session.query(Appointment, Patient, Doctor)
        .join(Patient, Appointment.patient_id == Patient.id)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .filter(Appointment.clinic_id == clinic.id, Appointment.date > today)
        .all()
    )

    return render_template(
        'clinic-dashboard.html',
        clinic=clinic,
        today_appointments=today_appointments,
        total_appointments=total_appointments,
        today_appointments_count=today_appointments_count,
        upcoming_appointments=upcoming_appointments,
        clinic_id=clinic.id
    )


@app.route('/calender', methods=['GET'], strict_slashes=False)
@login_required
@clinic_permission.require(http_exception=403)
def clinic_calender():
    return render_template('clinicCalender.html')


@app.route('/getcaldata', methods=['GET'], strict_slashes=False)
def clinic_cal():
    user = User.query.filter_by(id=current_user.id).first()
    if user is None:
        return translate('User not found'), 404
    clinic = Clinic.query.filter_by(user_id=current_user.id).first()
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
            'doctor': f'{" ".join(appointment.Doctor.users.name.split()[:2])}',
            'title': f'{" ".join(appointment.Doctor.users.name.split()[:2])}',
            'patient': f'{" ".join(appointment.Patient.users.name.split()[:2])}',
            'start': f'{appointment.Appointment.date}T{appointment.Appointment.time}',
            'end': f'{appointment.Appointment.date}T{appointment.Appointment.time}',
            'img': f'../static/images/doctors/{appointment.Doctor.users.photo}',
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
    rows_changed = Notification.query.filter_by(clinic_id=clinic_id).update(
        dict(isRead=True)
    )
    db.session.commit()
    return redirect(url_for('clinic_calender'))


### view all notifications page ###
@app.route('/notifications', methods=['GET', 'POST'], strict_slashes=False)
def all_notifications():
    if not current_user.is_authenticated or not hasattr(current_user, 'clinic'):
        return redirect(url_for('login_page'))
    clinic_id = current_user.clinic.id

    notifications = Notification.query.filter_by(clinic_id=clinic_id).all()

    current_time = datetime.now()
    processed_notifications = []

    for n in notifications:
        appointment = Appointment.query.get(n.appointment_id)
        if appointment:
            doctor = Doctor.query.get(appointment.doctor_id)
            patient = Patient.query.get(appointment.patient_id)

            if doctor and patient:
                processed_notifications.append(
                    {
                        'id': n.id,
                        'doctor': doctor.users.name
                        if doctor.users
                        else 'Unknown Doctor',
                        'patient': patient.users.name
                        if patient.users
                        else 'Unknown Patient',
                        'body': n.noteBody,
                        'isRead': n.isRead,
                        'time': n.time.strftime('%H:%M %p'),
                        'date': n.date.strftime('%d %B'),
                        'photo': doctor.users.photo if doctor.users else None,
                        'formatted_time': calculate_time_ago(current_time, n.notDate)
                    }
                )
    return render_template(
        'all_notifications.html', notifications=processed_notifications
    )


@app.route('/mark_as_read/<string:notification_id>', methods=['POST'])
def mark_as_read(notification_id):
    if not current_user.is_authenticated or not hasattr(current_user, 'clinic'):
        return jsonify({'success': False, 'message': 'User not authenticated'}), 403
    notification = Notification.query.get(notification_id)

    if notification and notification.clinic_id == current_user.clinic.id:
        notification.isRead = True
        db.session.commit()

        return jsonify({'success': True, 'message': 'Notification marked as read'}), 200
    else:
        return (
            jsonify(
                {'success': False, 'message': 'Notification not found or access denied'}
            ),
            404
        )


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/clinic_profile', methods=['GET', 'POST'])
@login_required
@clinic_permission.require(http_exception=403)
def clinic_profile():
    clinic = Clinic.query.filter_by(user_id=current_user.id).first_or_404()
    user = User.query.filter_by(id=current_user.id).first_or_404()
    govs = Governorate.query.filter().all()
    clinic_form = EditClinicForm(obj=clinic)
    user_form = EditUserForm(obj=user)
    clinic_form.gov_id.choices = [('', translate('Select a governorate'))] + [
        (gov.id, translate(gov.governorate_name)) for gov in govs
    ]
    if request.method == 'POST':
        if clinic_form.validate_on_submit():
            try:
                clinic_form.populate_obj(clinic)
                user_form.populate_obj(user)
                user.name = clinic_form.name.data
                file = request.files['photo']
                if file.filename:
                    # check from js code
                    if 'photo' in request.files:
                        unique_str = str(uuid.uuid4())[:8]
                        original_filename, extension = os.path.splitext(file.filename)
                        new_filename = (
                            f"{unique_str}_{user.name.replace(' ', '_')}{extension}"
                        )
                        user.photo = new_filename
                        if file and allowed_file(file.filename):
                            filename = secure_filename(new_filename)
                            file.save(
                                os.path.join(
                                    app.config['UPLOAD_FOLDER'], 'clinic', filename
                                )
                            )
                db.session.commit()
                flash('Data update successfully', category='success')
                return redirect(url_for('clinic_profile'))
            except Exception as e:
                flash(f'something wrong', category='danger')
                print(str(e))
        if clinic_form.errors != {}:
            for field_name, error_messages in clinic_form.errors.items():
                for err_msg in error_messages:
                    flash(
                        f"Error in {clinic_form[field_name].label.text}: {err_msg}",
                        category='danger'
                    )
        elif user_form.errors != {}:
            for field_name, error_messages in user_form.errors.items():
                for err_msg in error_messages:
                    flash(
                        f"Error in {user_form[field_name].label.text}: {err_msg}",
                        category='danger'
                    )
        return redirect(url_for('clinic_profile'))
    clinic_form.gov_id.data = clinic.governorate_id
    clinic_form.name.data = user.name

    return render_template(
        'clinic-profile-settings.html', user_form=user_form, clinic_form=clinic_form
    )

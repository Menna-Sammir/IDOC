from app import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from datetime import datetime
from sqlalchemy import func, asc
from flask import session
from datetime import date
from app.models.models import *
from flask_principal import Permission, RoleNeed
from app.views.forms.booking_form import AppointmentForm
from flask_login import login_required, current_user
from app import translate
from werkzeug.utils import secure_filename


admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))



# doctor dashboard page >>> view appointments today
@app.route('/doctor_dashboard', methods=['GET', 'POST'])
@login_required
@doctor_permission.require(http_exception=403)
def doctor_dash():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    print(doctor)
    if doctor is None:
        return translate('User is not a doctor'), 403
    
    form = AppointmentForm()
    appointments = Appointment.query.filter_by(date=date.today(), seen=False).order_by(asc(Appointment.time))
    if appointments.all():
        nextAppt = appointments.order_by(asc(Appointment.time)).first().id
    else:
        nextAppt = None
    monthAppointments = Appointment.query.filter(
        func.extract('month', Appointment.date) == datetime.now().month
    ).count()
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

    return render_template(
        'doctor-dashboard.html',
        doctor=doctor,
        appointments=appointments.all(),
        patient_count=patient_count,
        monthAppointments=monthAppointments,
        nextAppt = nextAppt,
        form=form
        )


### patient list
@app.route('/doctor_dashboard/patient_list', methods=['GET', 'POST'])
@login_required
@doctor_permission.require(http_exception=403)
def patient_list():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    if doctor is None:
        return translate('User is not a doctor'), 403

    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    patients = [appointment.patient for appointment in appointments]


    for patient in patients:
        user = User.query.filter_by(id=patient.user_id).first()
        patient.user_name = user.name if user else 'Unknown'

    return render_template('patient-list.html', doctor=doctor, patients=patients)


# @app.route('/patient_dashboard', methods=['GET', 'POST'])
# @login_required
# def patient_dash():
#     if current_user.patient:
#         patient = Patient.query.filter_by(user_id=current_user.id).first()
#         appointments = Appointment.query.filter_by(patient_id=patient.id).all()
#         return render_template('patient-dashboard.html', patient=patient, appointments=appointments)
    
#     elif current_user.doctor:
#         patient_id = request.args.get('patient_id')
#         if not patient_id:
#             flash('Patient ID is missing.', 'danger')
#             return redirect(url_for('doctor_dash'))

#         patient = Patient.query.get(patient_id)
#         if not patient:
#             flash('Patient not found', 'danger')
#             return redirect(url_for('doctor_dash'))
        
#         appointments = Appointment.query.filter_by(patient_id=patient.id).all()
#         return render_template('patient-dashboard.html', patient=patient,
#                                appointments=appointments,
#                                AppStatus=AppStatus)

#     else:
#         flash('Unauthorized access', 'danger')
#         return redirect(url_for('index'))


# @app.route('/update_follow_up', methods=['POST'])
# @login_required
# @doctor_permission.require(http_exception=403)
# def update_follow_up():
#     appointment_id = request.form.get('appointment_id')
#     follow_up_date_str = request.form.get('follow_up_date')
#     follow_up_time_str = request.form.get('follow_up_time')

#     appointment = Appointment.query.get_or_404(appointment_id)

#     try:
#         if follow_up_date_str and follow_up_time_str:
#             follow_up_date_time_str = f"{follow_up_date_str} {follow_up_time_str}"
#             follow_up_date = datetime.strptime(follow_up_date_time_str, '%Y-%m-%d %H:%M')
#         else:
#             follow_up_date = None

#         appointment_date = appointment.date
#         if isinstance(appointment_date, datetime):
#             appointment_date = appointment_date
#         else:
#             appointment_date = datetime.combine(appointment_date, datetime.min.time())

#         if follow_up_date and follow_up_date <= appointment_date:
#             flash('Follow-up date must be after the appointment date.', 'danger')
#             return redirect(url_for('patient_dash', patient_id=appointment.patient_id))

#         appointment.follow_up = follow_up_date
#         db.session.commit()
#         flash('Follow-up date updated successfully', 'success')
#         return redirect(url_for('patient_dash', patient_id=appointment.patient_id))

#     except ValueError:
#         flash('Invalid date format. Please try again.', 'danger')
#         return redirect(url_for('patient_dash', patient_id=appointment.patient_id))


# @app.route('/update_appointment_status', methods=['POST'])
# @login_required
# def update_appointment_status():
#     appointment_id = request.form.get('appointment_id')
#     new_status = request.form.get('new_status')

#     print(f"Received appointment_id: {appointment_id}, new_status: {new_status}")

#     if not appointment_id or not new_status:
#         return jsonify({'success': False, 'error': 'Missing appointment_id or new_status'}), 400

#     try:
#         new_status_enum = AppStatus[new_status]

#         appointment = Appointment.query.get(appointment_id)
#         if appointment:
#             appointment.status = new_status_enum
#             db.session.commit()
#             return jsonify({'success': True})
#         else:
#             return jsonify({'success': False, 'error': 'Appointment not found'}), 404

#     except KeyError:
#         print(f"Error: Invalid status received: {new_status}")
#         return jsonify({'success': False, 'error': 'Invalid status'}), 400
#     except Exception as e:
#         print(f"Error: {e}")
#         db.session.rollback()
#         return jsonify({'success': False, 'error': str(e)}), 500


# @app.route('/upload_medical_record', methods=['POST'])
# @login_required
# def upload_medical_record():
#     if current_user.doctor:
#         patient_id = request.form.get('patient_id')
#         description = request.form.get('description')
#         file = request.files.get('record_file')

#         if not patient_id or not description or not file:
#             flash('Missing required information.', 'danger')
#             return redirect(url_for('patient_dash', patient_id=patient_id))

#         patient = Patient.query.get(patient_id)
#         if not patient:
#             flash('Patient not found.', 'danger')
#             return redirect(url_for('doctor_dash'))

#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['PDF_UPLOAD_FOLDER'], filename)
#         file.save(file_path)

#         medical_record = MedicalRecord(
#             patient_id=patient.id,
#             description=description,
#             file_path=file_path,
#             created_by=current_user.id
#         )
#         db.session.add(medical_record)
#         db.session.commit()

#         flash('Medical record uploaded successfully.', 'success')
#         return redirect(url_for('patient_dash', patient_id=patient_id))

#     flash('Unauthorized access.', 'danger')
#     return redirect(url_for('index'))

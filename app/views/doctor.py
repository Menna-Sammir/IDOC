from app import app, db
from flask import render_template, redirect, url_for, flash, request
from datetime import datetime
from sqlalchemy import func, asc
from flask import session
from datetime import date
from app.models.models import *
from flask_principal import Permission, RoleNeed
from app.views.forms.booking_form import AppointmentForm
from app.views.forms.auth_form import EditUserForm
from app.views.forms.addDoctor_form import EditDoctorForm
from app.views.forms.Prescription_form import AddMedicineForm, MedicineForm
from flask_login import login_required, current_user
from app import translate
import os
from werkzeug.utils import secure_filename
import uuid

admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



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
    appointments = Appointment.query.filter_by(date=date.today(), seen=False).order_by(
        asc(Appointment.time)
    )
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
        nextAppt=nextAppt,
        form=form
    )


@app.route('/doctor_profile', methods=['GET', 'POST'])
@login_required
@doctor_permission.require(http_exception=403)
def doctor_profile():
    specializations = Specialization.query.filter().all()
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    user = User.query.filter_by(id=current_user.id).first_or_404()
    doctor_form = EditDoctorForm(obj=doctor)
    user_form = EditUserForm(obj=current_user)

    doctor_form.specialization_id.choices = [
        ('', translate('Select a specialization'))
    ] + [
        (specialization.id, translate(specialization.specialization_name))
        for specialization in specializations
    ]

    if request.method == 'POST':
        if doctor_form.validate_on_submit():
            try:
                doctor_form.populate_obj(doctor)
                user_form.populate_obj(user)
                user.name = (user_form.firstname.data + ' ' + user_form.lastname.data)
                doc_dur = int(doctor_form.duration.data) if doctor_form.duration.data is not None else 0
                doctor.duration = str(doc_dur * 100)
                file = request.files['photo']
                if file.filename:
                    #check from js code
                    if 'photo' in request.files:
                        unique_str = str(uuid.uuid4())[:8]
                        original_filename, extension = os.path.splitext(file.filename)
                        new_filename = f"{unique_str}_{current_user.name.replace(' ', '_')}{extension}"
                        user.photo = new_filename
                        if file and allowed_file(file.filename):
                            filename = secure_filename(new_filename)
                            file.save(
                                os.path.join(
                                    app.config['UPLOAD_FOLDER'], 'doctors', filename
                                )
                            )
                db.session.commit()
                flash('Data update successfully', category='success')
                return redirect(url_for('doctor_profile'))
            except Exception as e:
                flash(f'something wrong', category='danger')
                print(str(e))
        if doctor_form.errors != {}:
            for err_msg in doctor_form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
        elif user_form.errors != {}:
            for err_msg in user_form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
        return redirect(url_for('doctor_profile'))
    name_split = current_user.name.split()
    user_form.firstname.data = name_split[0]
    user_form.lastname.data = ' '.join(name_split[1:])
    minutes = doctor.duration.hour * 60 + doctor.duration.minute
    doctor_form.duration.data = str(minutes)
    return render_template(
        'doctor-profile-settings.html', user_form=user_form, doctor_form=doctor_form
    )

@app.route('/Prescription', methods=['GET', 'POST'])
@login_required
# @doctor_permission.require(http_exception=403)
def add_prescription():
    form = AddMedicineForm()
    patient_id = "ee57d6e4-1d31-4b8d-a615-55b4391ef8db"
    # patient_id = request.args.get("patient_id")
    if form.validate_on_submit():
        try:
            # MedicineTimes
            for item in form.items:
                med_exist = PatientMedicine.query.filter_by(medName=item.form.name.data).first()
                if not med_exist:
                    Patient_Medicine = PatientMedicine(
                        medName=item.form.name.data,
                        Quantity=item.form.quantity.data,
                        Date=datetime.now().strftime('%Y-%m-%d'),
                        patient_id=patient_id,
                        Added_By = current_user.id
                    )
                    db.session.add(Patient_Medicine)
                    current_medicine = Patient_Medicine
                    flash('Medicine added successfully', category='success')

                else:
                    med_exist.Quantity = item.form.quantity.data
                    med_exist.Days = item.form.Days.data
                    current_medicine = med_exist
                    MedicineTimes.query.filter_by(patient_medicine=med_exist).delete()
                    flash('Medicine updated successfully', category='success')
            for time_of_day in item.form.time_of_day.data:
                Medicine_Times = MedicineTimes(
                    patient_medicine=current_medicine,
                    time_of_day=time_of_day
                )
                db.session.add(Medicine_Times)
            db.session.commit()
            return redirect(url_for('add_prescription'))
        except Exception as e:
            db.session.rollback()
            flash(f'There was an error: {e}', category='danger')

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with adding medicine: {err_msg}', category='danger')

    return render_template('prescription.html', form=form)



### patient list
@app.route('/doctor_dashboard/patient_list', methods=['GET', 'POST'])
@login_required
@doctor_permission.require(http_exception=403)
def patient_list():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    if doctor is None:
        return translate('User is not a doctor'), 403

    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    patient_ids = set(appointment.patient_id for appointment in appointments)
    
    patients = Patient.query.filter(Patient.id.in_(patient_ids)).all()
    
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

from app import app, db, socketio
from flask import render_template, redirect, url_for, flash, request, jsonify
from app.models.models import *
from app.views.forms.checkout_form import checkoutForm
from app.views.forms.search_form import SearchForm
from app.views.forms.email_form import EmailForm
from app.views.forms.Prescription_form import AddMedicineForm
from sqlalchemy.orm import joinedload

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from flask import session
from flask_socketio import emit, join_room, leave_room
from app.views.forms.booking_form import AppointmentForm
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from app import translate, get_locale
import json
from flask_babel import lazy_gettext as _, format_decimal
from app import load_translations, translations
import secrets
from app.views.forms.patient_form import PatientForm
from werkzeug.utils import secure_filename
from flask_login import login_required
from flask import Flask, render_template
from app.models.models import db, Patient, User
from enum import Enum
from uuid import UUID
from flask_wtf.csrf import CSRFProtect
from flask_principal import Permission, RoleNeed
from sqlalchemy.orm import joinedload
from wtforms import SelectField, SubmitField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from app.views.forms.auth_form import EditUserForm
from app.views.forms.add_patient_history import PatientHistoryForm
import uuid

csrf = CSRFProtect(app)
doctor_permission = Permission(RoleNeed('doctor'))


@app.route('/')
@app.route('/home', methods=['GET', 'POST'], strict_slashes=False)
def home():
    try:
        form = SearchForm()
        E_form = EmailForm()

        # Get all specializations, regardless of whether they have doctors associated with them
        all_specializations = db.session.query(Specialization).all()

        # Get governorates that have clinics associated with doctors and same specialization
        governorates_with_clinics = (
            db.session.query(Governorate)
            .join(Clinic, Clinic.governorate_id == Governorate.id)
            .join(Doctor, Doctor.clinic_id == Clinic.id)
            .distinct()
            .all()
        )

        # Set the choices for the specialization dropdown with all specializations
        form.specialization.choices = [('', translate('Select a specialization'))] + [
            (s.id, translate(s.specialization_name)) for s in all_specializations
        ]

        # Set the choices for the governorate dropdown based on clinics that have doctors with the selected specialization
        form.governorate.choices = [('', translate('Select a governorate'))] + [
            (g.id, translate(g.governorate_name)) for g in governorates_with_clinics
        ]

        specialties = all_specializations
        doctors = Doctor.query.all()

        if request.method == 'POST':
            if form.validate_on_submit():
                session['specialization_id'] = form.specialization.data
                session['governorate_id'] = form.governorate.data
                session['doctor_name'] = form.doctor_name.data
                return redirect(url_for('search_doctor'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f'there was an error with creating a user: {err_msg}',
                    category='danger'
                )
        return render_template(
            'index.html',
            form=form,
            specialties=specialties,
            doctors=doctors,
            E_form=E_form
        )
    except Exception as e:
        db.session.rollback()
        raise e


@app.template_filter('basename')
def basename(path):
    return os.path.basename(path)


@app.route('/patient_dashboard', methods=['GET', 'POST'])
@login_required
def patient_dashboard():
    try:
        # Fetch patient details
        if current_user.patient:
            patient = Patient.query.filter_by(user_id=current_user.id).first()
            if not patient:
                flash('Patient not found', 'danger')
                return redirect(url_for('patient_dashboard'))
            patient_id = patient.id
        else:
            flash('Unauthorized access', 'danger')
            return redirect(url_for('home'))
        # Get next appointment

        Today_date = datetime.now().date()
        next_appointment_data = (
            db.session.query(Appointment)
            .join(Doctor, Appointment.doctor_id == Doctor.id)
            .join(Clinic, Doctor.clinic_id == Clinic.id)
            .join(Specialization, Doctor.specialization_id == Specialization.id)
            .filter(
                Appointment.patient_id == patient_id,
                Appointment.date >= Today_date,
                Appointment.seen == False,
                Appointment.status == AppStatus.Confirmed.value
            )
            .order_by(Appointment.date.asc(), Appointment.time.asc())
        )

        # Fetch prescriptions
        prescriptions_query = (
            db.session.query(PatientMedicine)
            .filter(PatientMedicine.patient_id == patient_id)
            .options(joinedload(PatientMedicine.medicine_times))
        )
        show_more_button = prescriptions_query.count() > 4

        form = PatientHistoryForm()
        if form.validate_on_submit():
            if form.details.data:
                file = form.details.data
                unique_str = str(uuid.uuid4())[:8]
                original_filename, extension = os.path.splitext(file.filename)
                new_filename = (
                    f"{unique_str}_{secure_filename(original_filename)}{extension}"
                )

                file.save(
                    os.path.join(
                        app.config['UPLOAD_FOLDER'], 'history_files', new_filename
                    )
                )

                new_history = PatientHistory(
                    details=new_filename,
                    type=form.type.data,
                    addedBy=current_user.id,
                    patient_id=patient_id
                )
                db.session.add(new_history)
                db.session.commit()
                flash('History record added successfully', 'success')
                return redirect(url_for('patient_dashboard', patient_id=patient_id))
        # Fetch patient history with file paths
        patient_history = (
            PatientHistory.query.filter_by(patient_id=patient_id)
            .options(joinedload(PatientHistory.user))
            .all()
        )

        return render_template(
            'patient-dashboard.html',
            next_appointments=next_appointment_data.all(),
            appointment=next_appointment_data.first(),
            prescriptions=prescriptions_query.limit(4).all(),
            show_more_button=show_more_button,
            patient_history=patient_history,
            form=form,
            AppStatus=AppStatus
        )
    except Exception as e:
        db.session.rollback()
        raise e


@app.route('/appointment_History', methods=['GET', 'POST'])
@login_required
def appointment_History():
    if current_user.patient:
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient:
            flash('Patient not found', 'danger')
            return redirect(url_for('patient_dashboard'))
        patient_id = patient.id
    elif current_user.doctor:
        patient_id = request.args.get('patient_id')
        if not patient_id:
            flash('Patient ID is missing', 'danger')
            return redirect(url_for('doctor_dash'))
        patient = Patient.query.get(patient_id)
        if not patient:
            flash('Patient not found', 'danger')
            return redirect(url_for('doctor_dash'))
    elif current_user.clinic:
        patient_id = request.args.get('patient_id')
        if not patient_id:
            flash('Patient ID is missing', 'danger')
            return redirect(url_for('clinic_dash'))
        patient = Patient.query.get(patient_id)
        if not patient:
            flash('Patient not found', 'danger')
            return redirect(url_for('clinic_dash'))
    else:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('home'))
    patient_histories = PatientHistory.query.filter_by(patient_id=patient_id).all()

    appointments = (
        db.session.query(Appointment)
        .join(Appointment.doctor)
        .join(Doctor.users)
        .options(joinedload(Appointment.doctor).joinedload(Doctor.users))
        .filter(Appointment.patient_id == patient_id)
        .all()
    )
    patient_histories = PatientHistory.query.filter_by(patient_id=patient_id).all()

    patient_medicines = PatientMedicine.query.filter_by(patient_id=patient_id).all()

    Medicine_form = AddMedicineForm()
    form = PatientHistoryForm()
    if request.method == 'POST':
        if Medicine_form.validate_on_submit():
            try:
                for item in Medicine_form.items:
                    med_exist = PatientMedicine.query.filter_by(
                        medName=item.form.name.data
                    ).first()
                    if not med_exist:
                        Patient_Medicine = PatientMedicine(
                            medName=item.form.name.data,
                            Quantity=item.form.quantity.data,
                            Date=datetime.now().strftime('%Y-%m-%d'),
                            patient_id=patient_id,
                            Added_By=current_user.id
                        )
                        db.session.add(Patient_Medicine)
                        current_medicine = Patient_Medicine
                        flash('Medicine added successfully', category='success')
                    else:
                        med_exist.Quantity = item.form.quantity.data
                        med_exist.Date = (datetime.now().strftime('%Y-%m-%d'),)
                        med_exist.Added_By = (current_user.id,)
                        current_medicine = med_exist
                        MedicineTimes.query.filter_by(
                            patient_medicine=med_exist
                        ).delete()
                        flash('Medicine updated successfully', category='success')
                    for time_of_day in item.form.time_of_day.data:
                        Medicine_Times = MedicineTimes(
                            patient_medicine=current_medicine, time_of_day=time_of_day
                        )
                        db.session.add(Medicine_Times)
                db.session.commit()
                return redirect(url_for('appointment_History', patient_id=patient_id))
            except Exception as e:
                db.session.rollback()
                flash(f'There was an error: {e}', category='danger')
            if Medicine_form.errors != {}:
                for err_msg in Medicine_form.errors.values():
                    flash(
                        f'There was an error with adding medicine: {err_msg}',
                        category='danger'
                    )
        if form.validate_on_submit():
            if form.details.data:
                file = form.details.data
                unique_str = str(uuid.uuid4())[:8]
                original_filename, extension = os.path.splitext(file.filename)
                new_filename = (
                    f"{unique_str}_{secure_filename(original_filename)}{extension}"
                )
                print(f"Saving file to: {new_filename}")
                file.save(
                    os.path.join(
                        app.config['UPLOAD_FOLDER'], 'history_files', new_filename
                    )
                )
                new_history = PatientHistory(
                    details=new_filename,
                    type=form.type.data,
                    addedBy=current_user.id,
                    patient_id=patient_id
                )
                db.session.add(new_history)
                db.session.commit()
                flash('History record added successfully', 'success')
                return redirect(url_for('appointment_History', patient_id=patient_id))
    patient_history_query = PatientHistory.query.filter_by(patient_id=patient_id).all()

    # Organize patient history data
    patient_history = [
        {
            'details': history.details,
            'type': history.type.value if history.type else 'Not Provided',
            'added_by': history.user.name,
            'file_link': url_for(
                'static', filename=f'images/history_files/{history.details}'
            )
            if history.details
            else None
        }
        for history in patient_history_query
    ]
    return render_template(
        'appointment-History.html',
        appointments=appointments,
        patient=patient,
        patient_medicines=patient_medicines,
        patient_history=patient_history,
        patient_histories=patient_histories,
        form=form,
        Medicine_form=Medicine_form
    )


MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_file_EXTENSIONS = {'pdf'}


def allowed_file_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_file_EXTENSIONS
    )


ALLOWED_photo_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_photo_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_photo_EXTENSIONS
    )


@app.route('/upload_report', methods=['POST'])
@login_required
@doctor_permission.require(http_exception=403)
def upload_report():
    appointment_id = request.form.get('appointment_id')
    diagnosis = request.form.get('diagnosis')
    report_file = request.files.get('file')
    print(f"Appointment ID: {appointment_id}")
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file_file(file.filename):
        if file.content_length > MAX_FILE_SIZE:
            flash('File exceeds maximum allowed size of 10MB', 'danger')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        filepath = os.path.join('app/static/pdfs', filename)

        try:
            file.save(filepath)
        except Exception as e:
            flash(f'Error saving file: {str(e)}')
            return redirect(request.url)
        appointment_id = request.form.get('appointment_id')
        diagnosis = request.form.get('diagnosis')

        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            flash('Appointment not found')
            return redirect(request.url)
        appointment.Report = filename
        appointment.Diagnosis = diagnosis

        db.session.commit()

        flash('Report uploaded successfully', 'success')
        return redirect(
            url_for('appointment_History', patient_id=appointment.patient_id)
        )
    flash('Invalid file type. Only PDF files are allowed.')
    return redirect(request.url)


@app.route('/cancel_appointment', methods=['POST'])
@login_required
def cancel_appointment():
    appointment_id = request.form.get('appointment_id')
    appointment = Appointment.query.get(appointment_id)

    if appointment is None:
        flash('Appointment not found', 'danger')
        return redirect(url_for('patient_dashboard'))
    # Check if the current user is the patient who made the appointment
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    if patient is None:
        flash('Patient record not found', 'danger')
        return redirect(url_for('patient_dashboard'))
    # Update status to Cancelled and mark as seen
    appointment.status = AppStatus.Cancelled.name  # Use Enum name
    appointment.seen = True
    db.session.commit()
    flash('Appointment cancelled successfully', 'success')

    return redirect(url_for('patient_dashboard'))


@app.route('/update_follow_up', methods=['POST'])
@login_required
@doctor_permission.require(http_exception=403)
def update_follow_up():
    appointment_id = request.form.get('appointment_id')
    follow_up_date_str = request.form.get('follow_up_date')
    follow_up_time_str = request.form.get('follow_up_time')

    appointment = Appointment.query.get_or_404(appointment_id)

    try:
        if follow_up_date_str and follow_up_time_str:
            follow_up_date_time_str = f"{follow_up_date_str} {follow_up_time_str}"
            follow_up_date = datetime.strptime(
                follow_up_date_time_str, '%Y-%m-%d %H:%M'
            )
        else:
            follow_up_date = None
        if appointment.status.name != 'Completed':
            flash(
                'Follow-up can only be added or updated for completed appointments.',
                'danger'
            )
            return redirect(
                url_for('appointment_History', patient_id=appointment.patient_id)
            )
        appointment_date = appointment.date
        if isinstance(appointment_date, datetime):
            appointment_date = appointment_date
        else:
            appointment_date = datetime.combine(appointment_date, datetime.min.time())
        if follow_up_date and follow_up_date <= appointment_date:
            flash('Follow-up date must be after the appointment date.', 'danger')
            return redirect(
                url_for('appointment_History', patient_id=appointment.patient_id)
            )
        appointment.follow_up = follow_up_date
        db.session.commit()
        flash('Follow-up date updated successfully', 'success')

        if current_user.doctor:
            return redirect(url_for('doctor_dash'))
        else:
            return redirect(
                url_for('appointment_History', patient_id=appointment.patient_id)
            )
    except ValueError:
        flash('Invalid date format. Please try again.', 'danger')
        return redirect(
            url_for('appointment_History', patient_id=appointment.patient_id)
        )


@app.route('/update_appointment_status', methods=['POST'])
@login_required
def update_appointment_status():
    appointment_id = request.form.get('appointment_id')
    new_status = request.form.get('new_status')

    print(f"Received appointment_id: {appointment_id}, new_status: {new_status}")

    if not appointment_id or not new_status:
        return (
            jsonify(
                {'success': False, 'error': 'Missing appointment_id or new_status'}
            ),
            400
        )
    try:
        new_status_enum = AppStatus[new_status]

        appointment = Appointment.query.get(appointment_id)
        if appointment:
            appointment.status = new_status_enum
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Appointment not found'}), 404
    except KeyError:
        print(f"Error: Invalid status received: {new_status}")
        return jsonify({'success': False, 'error': 'Invalid status'}), 400
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


#### doctor search page ####
@app.route('/search_doctor', methods=['GET', 'POST'], strict_slashes=False)
def search_doctor():
    specialization_id = session.get('specialization_id', None)
    governorate_id = session.get('governorate_id', None)
    doctor_name = session.get('doctor_name', None)

    page = request.args.get('page', 1, type=int)
    per_page = 10

    form = AppointmentForm()

    query = (
        db.session.query(Doctor, Specialization, Clinic, Governorate, User)
        .outerjoin(Specialization, Doctor.specialization_id == Specialization.id)
        .outerjoin(Clinic, Doctor.clinic_id == Clinic.id)
        .outerjoin(Governorate, Clinic.governorate_id == Governorate.id)
        .outerjoin(User, Doctor.user_id == User.id)
    )

    if request.method == 'GET':
        if specialization_id:
            query = query.filter(Doctor.specialization_id == specialization_id)
        if governorate_id:
            query = query.filter(Clinic.governorate_id == governorate_id)
        if doctor_name:
            query = query.filter(User.name.ilike(f'%{doctor_name}%'))
        specializations = Specialization.query.all()
        governorates = Governorate.query.all()

        session.pop('specialization_id', None)
        session.pop('governorate_id', None)
        session.pop('doctor_name', None)
    else:
        selected_specializations = request.form.getlist('select_specialization')
        selected_date = request.form.get('date')

        if selected_specializations:
            query = query.filter(Doctor.specialization_id.in_(selected_specializations))
        if selected_date:
            try:
                search_date = datetime.strptime(selected_date, '%d/%m/%Y').date()
                subquery = (
                    db.session.query(Doctor.id)
                    .outerjoin(
                        Appointment,
                        and_(
                            Doctor.id == Appointment.doctor_id,
                            func.date(Appointment.date) == search_date
                        )
                    )
                    .filter(Appointment.id == None)
                )
                query = query.filter(Doctor.id.in_(subquery))
            except ValueError:
                flash('Invalid date format', 'error')
        specializations = Specialization.query.all()
        governorates = Governorate.query.all()
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    doctors = pagination.items

    return render_template(
        'search.html',
        doctors=doctors,
        specializations=specializations,
        governorates=governorates,
        selected_specializations=selected_specializations
        if request.method == 'POST'
        else [],
        selected_date=selected_date if request.method == 'POST' else None,
        pagination=pagination,
        form=form
    )


@app.route('/book', methods=['GET', 'POST'])
def doctor_appointments():
    form = AppointmentForm()
    doctor_id = request.args.get('doctor_id')
    doctor = Doctor.query.get_or_404(doctor_id)
    specialization_name = doctor.specialization.specialization_name
    other_doctors = (
        Doctor.query.filter(
            Doctor.specialization_id == doctor.specialization_id, Doctor.id != doctor_id
        )
        .limit(3)
        .all()
    )

    # Generate upcoming dates with format (date, day_of_week, day_of_month)
    dates = [
        (
            (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'),
            (datetime.now() + timedelta(days=i)).strftime('%a'),
            (datetime.now() + timedelta(days=i)).strftime('%d')
        )
        for i in range(9)
    ]

    timeslots_by_date = {}

    # Convert duration from TIME to timedelta
    duration = timedelta(hours=doctor.duration.hour, minutes=doctor.duration.minute)

    for date, _, _ in dates:
        daily_timeslots = []
        start_time = datetime.combine(
            datetime.strptime(date, '%Y-%m-%d').date(), doctor.From_working_hours
        )
        end_time = datetime.combine(
            datetime.strptime(date, '%Y-%m-%d').date(), doctor.To_working_hours
        )

        if start_time > end_time:
            end_time += timedelta(
                days=1
            )  # Handle cases where end time is on the next day
        current_time = start_time

        # Generate timeslots
        while current_time + duration <= end_time:
            timeslot = f"{current_time.strftime('%I:%M %p')}"
            daily_timeslots.append((timeslot, timeslot))  # Only include start time
            current_time += duration
        # Filter out booked timeslots
        existing_appointments = Appointment.query.filter_by(
            doctor_id=doctor.id, date=date
        ).all()

        # Ensure the date and time formats match the ones used in the form
        booked_timeslots = [
            f"{a.date.strftime('%Y-%m-%d')} {a.time.strftime('%I:%M %p')}"
            for a in existing_appointments
        ]

        # Mark timeslots as available or booked
        available_timeslots = []
        for timeslot in daily_timeslots:
            # Compare time without the date part
            is_available = f"{date} {timeslot[0]}" not in booked_timeslots
            available_timeslots.append((timeslot[0], timeslot[1], is_available))
        timeslots_by_date[date] = available_timeslots
    if request.method == 'POST':
        selected_timeslot = request.form.get('timeslot')

        if not selected_timeslot:
            flash('Please select a time slot before continuing.', 'primary')
            return redirect(request.url)
        try:
            date_str, start_time_str = selected_timeslot.split(' ', 1)
            start_time = datetime.strptime(start_time_str, '%I:%M %p').time()

            end_time = (
                datetime.combine(datetime.strptime(date_str, '%Y-%m-%d'), start_time)
                + duration
            ).time()

            session['doctor_id'] = doctor_id
            session['date'] = date_str
            session['start_time'] = start_time_str
            session['end_time'] = end_time.strftime('%I:%M %p')
            return redirect(url_for('patient_checkout'))
        except ValueError:
            flash('Invalid time slot format. Please try again.', 'danger')
            return redirect(request.url)
    return render_template(
        'booking.html',
        form=form,
        doctor=doctor,
        dates=dates,
        timeslots_by_date=timeslots_by_date,
        specialization_name=specialization_name,
        other_doctors=other_doctors
    )


@app.route('/checkout', methods=['GET', 'POST'], strict_slashes=False)
def patient_checkout():
    try:
        checkout_form = checkoutForm()
        doctor_id = session.get('doctor_id', None)
        date_str = session.get('date', None)
        start_time = session.get('start_time', None)
        end_time = session.get('end_time', None)

        date = datetime.strptime(date_str, '%Y-%m-%d')
        start_time = datetime.strptime(start_time, '%I:%M %p').time()

        doctor_data = Doctor.query.filter_by(id=doctor_id).first()

        if doctor_data:
            clinic_data = doctor_data.clinic
            gov = clinic_data.governorate

            if request.method == 'POST':
                confirm_message = ''
                user_to_create = None
                name = ''
                status = AppStatus.Confirmed

                if checkout_form.validate_on_submit():
                    temp_password = secrets.token_urlsafe(8)

                    role = Role.query.filter_by(role_name='patient').first().id
                    patient_user = (
                        User.query.filter_by(email=checkout_form.email_address.data)
                        .join(UserRole)
                        .filter(UserRole.role_id == role)
                        .first()
                    )

                    if patient_user:
                        name = patient_user.name
                        patient_create = Patient.query.filter_by(
                            user_id=patient_user.id
                        ).first()
                        status = AppStatus.Confirmed
                    else:
                        reset_link = url_for(
                            'reset_password',
                            email=checkout_form.email_address.data,
                            _external=True
                        )
                        confirm_message = f"To confirm your appointment please login temporary password is: {temp_password}\n\nUse this link to reset your password:<a href=' {reset_link}'>click Here</a>"
                        name = f"{checkout_form.firstname.data} {checkout_form.lastname.data}"
                        user_to_create = User(
                            name=name,
                            email=checkout_form.email_address.data,
                            activated=False,
                            temp_pass=temp_password
                        )
                        patient_create = Patient(
                            phone=checkout_form.phone.data, users=user_to_create
                        )
                        role_to_create = UserRole(role_id=role, user=user_to_create)
                        db.session.add(patient_create)
                        db.session.add(role_to_create)
                    appointment_create = Appointment(
                        date=date.strftime('%Y-%m-%d'),
                        time=start_time.strftime('%H:%M:%S'),
                        seen=False,
                        clinic_id=clinic_data.id,
                        patient=patient_create,
                        doctor_id=doctor_id,
                        status=status
                    )

                    logo_path = os.path.join(app.root_path, 'static', 'img', 'logo.png')

                    message_body = f"""







                    <html>







                        <head>







                            <style>







                                body {{







                                    font-family: Arial, sans-serif;







                                    font-size: 18px;







                                    margin: 0;







                                    padding: 0;







                                    background-color: #f4f4f4;







                                }}







                                .container {{







                                    width: 80%;







                                    margin: 20px auto;







                                    background-color: #fff;







                                    padding: 20px;







                                    border-radius: 10px;







                                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);







                                }}







                                .header {{







                                    background-color: #007bff;







                                    padding: 10px;







                                    text-align: center;







                                    border-radius: 10px 10px 0 0;







                                }}







                                .logo {{







                                    text-align: center;







                                    margin-bottom: 20px;







                                }}







                                .content {{







                                    padding: 20px;







                                }}







                                .footer {{







                                    text-align: left;







                                    margin-top: 20px;







                                    color: #777;







                                }}







                                a {{







                                    color: red;







                                }}







                            </style>







                        </head>







                        <body>







                            <div class="container">







                                <div class="header">







                                    <h2>Appointment Confirmation</h2>







                                </div>







                                <img src="cid:logo_image" alt="Your Logo" width="200">







                                <div class="content">







                                    <p>Dear {name},</p>







                                    <p>We are writing to confirm your upcoming appointment at {clinic_data.users.name}.</p>







                                    <h3>Appointment Details:</h3>







                                    <ul>







                                        <li><strong>Date:</strong> {date.strftime('%d %b %Y')}</li>







                                        <li><strong>Time:</strong> from {start_time.strftime("%H:%M:%S")} to {end_time} </li>







                                        <li><strong>Doctor:</strong> {doctor_data.users.name}</li>







                                        <li><strong>Location:</strong> {clinic_data.address}, {gov.governorate_name}</li>







                                    </ul>







                                    <p>Please arrive 10-15 minutes early to complete any necessary paperwork.</p>







                                    <p>If you need to reschedule or have any questions, feel free to contact us at {clinic_data.phone} or reply to this email.</p>







                                    <p>We look forward to seeing you and providing the care you need.</p>







                                    <a>{confirm_message}</a>







                                </div>







                                <div class="footer">







                                    <p>Best regards,</p>







                                    <p>{clinic_data.users.name}</p>







                                    <p>{clinic_data.phone}</p>







                                </div>







                            </div>







                        </body>







                    </html>







                    """

                    message_create = Message(
                        appointment=appointment_create, status=False
                    )

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    email_address = os.getenv('EMAIL_ADDRESS')
                    app_password = os.getenv('APP_PASSWORD')
                    server.login(email_address, app_password)
                    msg = MIMEMultipart()
                    msg['From'] = email_address
                    msg['To'] = checkout_form.email_address.data
                    msg[
                        'Subject'
                    ] = f'Appointment Confirmation - {clinic_data.users.name}'
                    message = message_body
                    msg.attach(MIMEText(message, 'html'))
                    with open(logo_path, 'rb') as f:
                        logo_data = f.read()
                    logo_part = MIMEImage(logo_data)
                    logo_part.add_header('Content-ID', '<logo_image>')
                    msg.attach(logo_part)
                    server.send_message(msg)
                    server.quit()
                    message_create.status = True

                    notification_create = Notification(
                        clinic_id=clinic_data.id,
                        date=date.strftime('%Y-%m-%d'),
                        time=start_time.strftime('%H:%M:%S'),
                        noteBody='has booked appointment to Dr.',
                        isRead=False,
                        appointment=appointment_create
                    )

                    db.session.add(appointment_create)
                    db.session.add(notification_create)
                    db.session.commit()

                    socketio.emit(
                        'appointment_notification',
                        {
                            'doctor': doctor_data.users.name,
                            'date': date.strftime('%d %b %Y'),
                            'time': start_time.strftime('%H:%M:%S'),
                            'patient': patient_create.users.name,
                            'photo': doctor_data.users.photo
                        },
                        room=clinic_data.id,
                        namespace='/'
                    )
                    session['doctor'] = doctor_data.users.name
                    session['date'] = date.strftime('%d %b %Y')
                    session['start_time'] = start_time.strftime('%H:%M:%S')
                    session['end_time'] = end_time
                    session['clinic_id'] = clinic_data.id

                    return redirect(url_for('checkout_success'))
                if checkout_form.errors != {}:
                    for err_msg in checkout_form.errors.values():
                        flash(
                            translate(
                                f'there was an error with creating a user: {err_msg}'
                            ),
                            category='danger'
                        )
        else:
            flash('No doctor data found', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Something went wrong: {str(e)}', 'danger')
    return render_template(
        'checkout.html',
        doctor=doctor_data,
        clinic=clinic_data,
        gov=gov,
        date=date.strftime('%d %b %Y'),
        start_time=start_time.strftime('%H:%M'),
        end_time=end_time,
        form=checkout_form
    )


def send_appointment_notification(clinic_id, data):
    socketio.emit('appointment_notification', data, room=clinic_id)


@socketio.on('connect')
def handle_connect():
    clinic_id = request.args.get('clinic_id')
    print(f"Clinic ID: {clinic_id}")
    if clinic_id:
        join_room(clinic_id)
        emit('connected', {'message': 'Connected to clinic ' + clinic_id})


@socketio.on('disconnect')
def handle_disconnect():
    clinic_id = getattr(current_user.clinic, 'id', None)
    if clinic_id:
        leave_room(clinic_id)


@app.route('/checkout-success', methods=['GET'], strict_slashes=False)
def checkout_success():
    doctor = session.get('doctor', None)
    date = session.get('date', None)
    start_time = session.get('start_time', None)
    session.pop('doctor', None)
    session.pop('date', None)
    session.pop('start_time', None)
    return render_template(
        'booking-success.html', doctor=doctor, date=date, time=start_time
    )


@app.route('/email', methods=['POST'], strict_slashes=False)
def sendEmail():
    form = EmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                email_address = os.getenv('EMAIL_ADDRESS')
                app_password = os.getenv('APP_PASSWORD')
                server.login(email_address, app_password)
                logo_path = os.path.join(app.root_path, 'static', 'img', 'logo.png')
                msg = MIMEMultipart()
                msg['From'] = form.email_address.data
                msg['To'] = email_address
                msg['Subject'] = form.subject.data
                message_body = f"""<html>



                    <head>



                        <style>



                            body {{



                                font-family: Arial, sans-serif;



                                font-size: 18px;



                                margin: 0;



                                padding: 0;



                                background-color: #f4f4f4;



                            }}



                            .container {{



                                width: 80%;



                                margin: 20px auto;



                                background-color: #fff;



                                padding: 20px;



                                border-radius: 10px;



                                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);



                            }}



                            p{{



                                font-size:16px;



                            }}



                            .logo {{



                                text-align: center;



                                margin-bottom: 20px;



                            }}



                            .content {{



                                padding: 20px;



                            }}



                        </style>



                    </head>



                    <body>



                        <div class="container">



                                <img src="cid:logo_image" alt="Your Logo" width="200">



                            </div>



                            <div class="content">



                                <p>{form.message.data}</p>



                            </div>



                        </div>



                    </body>



                    </html>



                """
                message = message_body
                msg.attach(MIMEText(message, 'html'))
                with open(logo_path, 'rb') as f:
                    logo_data = f.read()
                logo_part = MIMEImage(logo_data)
                logo_part.add_header('Content-ID', '<logo_image>')
                msg.attach(logo_part)

                server.send_message(msg)
                server.quit()
                flash(f'email sent successfully', category='success')
            except Exception as e:
                flash(f'something wrong', category='danger')
                print(str(e))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'there was an error with creating a user: {err_msg}', category='danger'
            )
    return redirect(url_for('home'))


## patient setting to edit patient profile ###
@app.route('/patient_setting', methods=['GET', 'PUT'])
@login_required
def patient_setting():
    user = User.query.filter_by(id=current_user.id).first()
    patient = Patient.query.filter_by(user_id=current_user.id).first()

    form = PatientForm(
        firstname=user.name.split()[0] if user.name else '',
        lastname=user.name.split()[1]
        if user.name and len(user.name.split()) > 1
        else '',
        email=user.email,
        phone=patient.phone if patient else '',
        address=patient.address if patient else '',
        governorate=patient.governorate_id if patient else None,
        age=patient.age if patient else None,
        blood_group=patient.blood_group.name
        if patient and patient.blood_group
        else None,
        allergy=patient.allergy.name if patient and patient.allergy else None
    )

    if request.method == 'PUT':
        if form.validate():
            if form.photo.data:
                file = request.files['photo']
                print(file)
                if 'photo' in request.files:
                    unique_str = str(uuid.uuid4())[:8]
                    _, extension = os.path.splitext(file.filename)
                    new_filename = (
                        f"{unique_str}_{current_user.name.replace(' ', '_')}{extension}"
                    )
                    user.photo = new_filename
                    if file and allowed_photo_file(file.filename):
                        filename = secure_filename(new_filename)
                        file.save(
                            os.path.join(
                                app.config['UPLOAD_FOLDER'], 'patients', filename
                            )
                        )
            email_exists = User.query.filter(
                User.email == form.email.data, User.id != user.id
            ).first()
            if email_exists:
                return (
                    jsonify(
                        {'status': 'error', 'message': 'Email address already exists!'}
                    ),
                    400
                )
            if not patient:
                patient = Patient(user_id=current_user.id)
            patient.firstname = form.firstname.data
            patient.lastname = form.lastname.data
            user.email = form.email.data
            patient.phone = form.phone.data
            patient.address = form.address.data
            patient.governorate_id = form.governorate.data
            patient.age = form.age.data
            patient.blood_group = form.blood_group.data
            patient.allergy = form.allergy.data

            user.name = f"{form.firstname.data} {form.lastname.data}"
            user.email = form.email.data

            try:
                db.session.add(patient)
                db.session.add(user)
                db.session.commit()
                flash('Your profile has been updated!', 'success')
                return jsonify({'status': 'success'})
            except Exception as e:
                db.session.rollback()
                return (
                    jsonify(
                        {
                            'status': 'error',
                            'message': 'An error occurred while updating your settings. Please try again.'
                        }
                    ),
                    500
                )
        errors = {field: errors[0] for field, errors in form.errors.items()}
        return jsonify({'status': 'error', 'errors': errors}), 400
    return render_template(
        'patient-setting.html', form=form, patient=patient, user=user
    )

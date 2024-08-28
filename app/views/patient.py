from app import app, db, socketio
from flask import render_template, redirect, url_for, flash, request
from app.models.models import *
from app.views.forms.checkout_form import checkoutForm
from app.views.forms.search_form import SearchForm
from app.views.forms.email_form import EmailForm
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


def convert_to_24_hour(time_str):
    return datetime.strptime(time_str, '%I:%M %p').time()


@app.route('/')
@app.route('/home', methods=['GET', 'POST'], strict_slashes=False)
def home():
    form = SearchForm()
    E_form = EmailForm()

    form.specialization.choices = [('', translate('Select a specialization'))] + [
        (s.id, translate(s.specialization_name)) for s in Specialization.query.all()
    ]

    form.governorate.choices = [('', translate('Select a governorate'))] + [
        (g.id, translate(g.governorate_name)) for g in Governorate.query.all()
    ]

    specialties = Specialization.query.filter().all()
    doctor = Doctor.query.filter().all()
    if request.method == 'POST':
        if form.validate_on_submit():
            session['specialization_id'] = form.specialization.data
            session['governorate_id'] = form.governorate.data
            session['doctor_name'] = form.doctor_name.data
            return redirect(url_for('search_doctor'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'there was an error with creating a user: {err_msg}', category='danger'
            )
    return render_template(
        'index.html', form=form, specialties=specialties, doctors=doctor, E_form=E_form
    )


# doctor search page
@app.route('/search_doctor', methods=['GET', 'POST'], strict_slashes=False)
def search_doctor():
    specialization_id = session.get('specialization_id', None)
    governorate_id = session.get('governorate_id', None)
    doctor_name = session.get('doctor_name', None)

    page = request.args.get('page', 1, type=int)
    per_page = 10

    form = AppointmentForm()

    query = (
        db.session.query(Doctor, Specialization, Clinic, Governorate)
        .outerjoin(Specialization, Doctor.specialization_id == Specialization.id)
        .outerjoin(Clinic, Doctor.clinic_id == Clinic.id)
        .outerjoin(Governorate, Clinic.governorate_id == Governorate.id)
    )

    if request.method == 'GET':
        if specialization_id:
            query = query.filter(Doctor.specialization_id == specialization_id)
        if governorate_id:
            query = query.filter(Clinic.governorate_id == governorate_id)
        if doctor_name:
            query = query.filter(Doctor.name.ilike(f'%{doctor_name}%'))
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
    clinic = doctor.clinic
    specialization_name = doctor.specialization.specialization_name
    other_doctors = (
        Doctor.query.filter(
            Doctor.specialization_id == doctor.specialization_id, Doctor.id != doctor_id
        )
        .limit(3)
        .all()
    )
    dates = []
    for i in range(9):
        date = datetime.now() + timedelta(days=i)
        dates.append(
            (date.strftime('%Y-%m-%d'), date.strftime('%a'), date.strftime('%d'))
        )
    timeslots_by_date = {}
    for date in dates:
        daily_timeslots = []
        start_hour = doctor.From_working_hours.hour
        end_hour = doctor.To_working_hours.hour

        if start_hour > end_hour:
            end_hour += 24

        for hour in range(start_hour, end_hour):
            start_time = datetime.strptime(f"{hour % 24}:00", '%H:%M').time()
            end_time = datetime.strptime(f"{(hour + 1) % 24}:00", '%H:%M').time()

            if start_time.strftime('%p') == 'AM' and hour >= 24:
                break  

            timeslot = f"{date[0]} {start_time.strftime('%I:%M %p')}-{end_time.strftime('%I:%M %p')}"
            daily_timeslots.append(
                (
                    timeslot,
                    f"{start_time.strftime('%I:%M %p')}-{end_time.strftime('%I:%M %p')}"
                )
            )
        existing_appointments = Appointment.query.filter_by(
            doctor_id=doctor.id, date=date[0]
        ).all()
        booked_timeslots = [
            f"{a.date.strftime('%Y-%m-%d')} {a.time.strftime('%I:%M %p')}-"
            f"{(datetime.combine(a.date, a.time) + timedelta(hours=1)).time().strftime('%I:%M %p')}"
            for a in existing_appointments
        ]
        available_timeslots = []
        for timeslot in daily_timeslots:
            if timeslot[0] in booked_timeslots:
                available_timeslots.append((timeslot[0], timeslot[1], False))
            else:
                available_timeslots.append((timeslot[0], timeslot[1], True))
        timeslots_by_date[date[0]] = available_timeslots
    if request.method == 'POST':
        selected_timeslot = request.form.get('timeslot')
        if not selected_timeslot:
            flash('Please select a time slot before continuing.', 'primary')
            return redirect(request.url)
        
        try:
            date_str, time_range = selected_timeslot.split(' ', 1)
            start_time_str, end_time_str = time_range.split('-')
            start_time_str = start_time_str.strip()
            end_time_str = end_time_str.strip()
            start_time = datetime.strptime(start_time_str, '%I:%M %p').time()
            end_time = datetime.strptime(end_time_str, '%I:%M %p').time()
        except ValueError:
            flash('Invalid time slot format. Please try again.', 'danger')
            return redirect(request.url)
        print(selected_timeslot)
        print(date_str)
        print(start_time)
        print(end_time)
        session['doctor_id'] = doctor_id
        session['date'] = date_str
        session['start_time'] = start_time_str
        session['end_time'] = end_time_str
        return redirect(url_for('patient_checkout'))
    return render_template(
        'booking.html',
        form=form,
        doctor=doctor,
        dates=dates,
        timeslots_by_date=timeslots_by_date,
        clinic=clinic,
        specialization_name=specialization_name,
        other_doctors=other_doctors
    )


@app.route('/checkout', methods=['GET', 'POST'], strict_slashes=False)
def patient_checkout():
    checkout_form = checkoutForm()
    doctor_id = session.get('doctor_id', None)
    date_str = session.get('date', None)
    start_time_str = session.get('start_time', None)
    end_time_str = session.get('end_time', None)
    date = datetime.strptime(date_str, '%Y-%m-%d')
    start_time = datetime.strptime(start_time_str, '%I:%M %p').time()
    end_time = datetime.strptime(end_time_str, '%I:%M %p').time()


    doctor_data = Doctor.query.filter_by(id=doctor_id).first()
    if doctor_data:
        clinic_data = doctor_data.clinic
        gov = clinic_data.governorate
        if request.method == 'POST':
            if checkout_form.validate_on_submit():
                patient = Patient.query.filter_by(
                    email=checkout_form.email_address.data
                ).first()
                if patient:
                    patient_create = patient
                else:
                    patient_create = Patient(
                        name=checkout_form.firstname.data
                        + ' '
                        + checkout_form.lastname.data,
                        phone=checkout_form.phone.data,
                        email=checkout_form.email_address.data
                    )
                appointment_create = Appointment(
                    date=date.strftime('%Y-%m-%d'),
                    time=start_time.strftime('%H:%M:%S'),
                    status=True,
                    seen=False,
                    clinic_id=clinic_data.id,
                    patient=patient_create,
                    doctor_id=doctor_id
                )
                logo_path = os.path.join(app.root_path, 'static', 'img', 'logo.png')
                message_create = Message(
                    message_body=f"""\

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

                </style>

            </head>

            <body>

                <div class="container">

                    <div class="header">

                        <h2>Appointment Confirmation</h2>

                    </div>

                        <img src="cid:logo_image" alt="Your Logo" width="200">

                    </div>

                    <div class="content">

                        <p>Dear {patient_create.name},</p>

                        <p>We are writing to confirm your upcoming appointment at {clinic_data.name}.</p>

                        <h3>Appointment Details:</h3>

                        <ul>

                            <li><strong>Date:</strong> {date.strftime('%d %b %Y')}</li>

                            <li><strong>Time:</strong>from {start_time.strftime("%H:%M:%S")} to {end_time.strftime("%H:%M:%S")}</li>

                            <li><strong>Doctor:</strong> {doctor_data.name}</li>

                            <li><strong>Location:</strong> {clinic_data.address}, {gov.governorate_name}</li>

                        </ul>

                        <p>Please arrive 10-15 minutes early to complete any necessary paperwork.</p>

                        <p>If you need to reschedule or have any questions, feel free to contact us at {clinic_data.phone} or reply to this email.</p>

                        <p>We look forward to seeing you and providing the care you need.</p>

                    </div>

                    <div class="footer">

                        <p>Best regards,</p>

                        <p>{clinic_data.name}</p>

                        <p>{clinic_data.phone}</p>

                    </div>

                </div>

            </body>

            </html>

            """,
                    appointment=appointment_create,
                    status=False
                )
                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    email_address = os.getenv('EMAIL_ADDRESS')
                    app_password = os.getenv('APP_PASSWORD')
                    server.login(email_address, app_password)
                    msg = MIMEMultipart()
                    msg['From'] = email_address
                    msg['To'] = checkout_form.email_address.data
                    msg['Subject'] = f'Appointment Confirmation - {clinic_data.name}'
                    message = message_create.message_body
                    msg.attach(MIMEText(message, 'html'))
                    with open(logo_path, 'rb') as f:
                        logo_data = f.read()
                    logo_part = MIMEImage(logo_data)
                    logo_part.add_header('Content-ID', '<logo_image>')
                    msg.attach(logo_part)
                    server.send_message(msg)
                    server.quit()
                    message_create.status = True
                except Exception as e:
                    flash(f'something wrong', category='danger')
                    print(str(e))
                notification_create = Notification(
                    clinic_id=clinic_data.id,
                    date=date.strftime('%Y-%m-%d'),
                    time=start_time.strftime('%H:%M:%S'),
                    noteBody='has booked appointment to Dr.',
                    isRead=False,
                    appointment=appointment_create
                )
                db.session.add(patient_create)
                db.session.add(appointment_create)
                db.session.add(message_create)
                db.session.add(notification_create)
                db.session.commit()
                socketio.emit(
                    'appointment_notification',
                    {
                        'doctor': doctor_data.name,
                        'date': date.strftime('%d %b %Y'),
                        'time': start_time.strftime('%H:%M:%S'),
                        'patient': patient_create.name,
                        'photo': doctor_data.photo
                    },
                    room=clinic_data.id,
                    namespace='/'
                )
                session['doctor'] = doctor_data.name
                session['date'] = date.strftime('%d %b %Y')
                session['start_time'] = start_time.strftime('%H:%M:%S')
                session['clinic_id'] = clinic_data.id

                return redirect(url_for('checkout_success'))
            if checkout_form.errors != {}:
                for err_msg in checkout_form.errors.values():
                    flash(
                        translate(
                            'there was an error with creating a user: {err_msg}'.format(
                                err_msg=err_msg
                            )
                        ),
                        category='danger'
                    )
    else:
        flash(f'no doctor data found', category='danger')
    return render_template(
        'checkout.html',
        doctor=doctor_data,
        clinic=clinic_data,
        gov=gov,
        date=date.strftime('%d %b %Y'),
        start_time=start_time.strftime('%H:%M'),
        end_time=end_time.strftime('%H:%M'),
        form=checkout_form
    )
def send_appointment_notification(clinic_id, data):
    socketio.emit('appointment_notification', data, room=clinic_id)
    
    
@socketio.on('connect')
def handle_connect():
    clinic_id = session.get('clinic_id')
    if clinic_id:
        join_room(clinic_id)
        emit('connected', {'message': 'Connected to clinic ' + clinic_id})


@socketio.on('disconnect')
def handle_disconnect():
    clinic_id = session.get('clinic_id')
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
                message_body = f"""\

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




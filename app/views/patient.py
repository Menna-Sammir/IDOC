from app import app, db, principal
from flask import render_template, redirect, url_for, flash, request, current_app
from app.models.models import *
from app.views.forms.checkout_form import checkoutForm
from app.views.forms.addClinic_form import ClinicForm
from app.views.forms.addDoctor_form import DoctorForm
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from datetime import datetime
from flask import session
from werkzeug.utils import secure_filename
import uuid


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add_clinic', methods=['GET', 'POST'], strict_slashes=False)
def add_clinic():
    add_clinic_form = ClinicForm()
    govs = Governorate.query.filter().all()
    add_clinic_form.gov_id.choices = [('', 'Select a governorate')] + [
        (gov.id, gov.governorate_name) for gov in govs
    ]
    if request.method == 'POST':
        try:
            clinic = Clinic.query.filter_by(
                name=add_clinic_form.clinicName.data
            ).first()
            if clinic:
                flash('clinic already exists!')
            else:
                if add_clinic_form.validate_on_submit():
                    from_hour = add_clinic_form.fromHour.data.strftime('%H:%M %p')
                    to_hour = add_clinic_form.toHour.data.strftime('%H:%M %p')
                    Clinic_create = Clinic(
                        name=add_clinic_form.clinicName.data,
                        phone=add_clinic_form.phone.data,
                        email=add_clinic_form.email_address.data,
                        address=add_clinic_form.clinicAddress.data,
                        working_hours=f'from {from_hour} to {to_hour}',
                        governorate_id=add_clinic_form.gov_id.data
                    )

                    if 'logo' not in request.files:
                        flash('No file part')
                        return redirect(request.url)
                    file = request.files['logo']
                    if file.filename == '':
                        flash('No selected file')
                        return redirect(request.url)
                    unique_str = str(uuid.uuid4())[:8]
                    original_filename, extension = os.path.splitext(file.filename)
                    new_filename = (
                        f"{unique_str}_{add_clinic_form.clinicName.data}{extension}"
                    )
                    Clinic_create.photo = new_filename
                    if file and allowed_file(file.filename):
                        filename = secure_filename(new_filename)
                        file.save(
                            os.path.join(app.config['UPLOAD_FOLDER'], 'clinic', filename)
                        )
                    db.session.add(Clinic_create)
                    db.session.commit()
                    return redirect(url_for('admin_dash'))
                if add_clinic_form.errors != {}:
                    for err_msg in add_clinic_form.errors.values():
                        flash(
                            f'there was an error with creating a user: {err_msg}',
                            category='danger'
                        )
        except Exception as e:
            flash(f'something wrong', category='danger')
            print(str(e))
    return render_template('add-clinic.html', form=add_clinic_form)


@app.route('/add_doctor', methods=['GET', 'POST'], strict_slashes=False)
def add_doctor():
    add_doctor_form = DoctorForm()
    clinics = Clinic.query.filter().all()
    specializations = Specialization.query.filter().all()
    add_doctor_form.clinic_id.choices = [('', 'Select a clinic')] + [
        (clinic.id, clinic.name) for clinic in clinics
    ]
    add_doctor_form.specialization_id.choices = [('', 'Select a specialization')] + [
        (specialization.id, specialization.specialization_name)
        for specialization in specializations
    ]
    if request.method == 'POST':
        if add_doctor_form.validate_on_submit():
            doctor_name = add_doctor_form.firstname.data + ' ' + add_doctor_form.lastname.data,
            doctor = Doctor.query.filter_by(
                name=doctor_name, clinic_id =add_doctor_form.clinic_id.data
            ).first()

            if doctor:
                flash('doctor already exists!')
            else:
                try:
                    clinic = Clinic.query.get(add_doctor_form.clinic_id.data).name
                    Doctor_create = Doctor(
                    name = doctor_name,
                    phone = add_doctor_form.phone.data,
                    email = add_doctor_form.email_address.data,
                    price = add_doctor_form.price.data,
                    specialization_id = add_doctor_form.specialization_id.data,
                    clinic_id = add_doctor_form.clinic_id.data
                    )
                    if 'photo' not in request.files:
                        flash('No file part')
                        return redirect(request.url)
                    file = request.files['photo']
                    if file.filename == '':
                        flash('No selected file')
                        return redirect(request.url)
                    unique_str = str(uuid.uuid4())[:8]
                    original_filename, extension = os.path.splitext(file.filename)
                    new_filename = (
                        f"{unique_str}_{clinic}_{doctor_name.strip()}{extension}"
                    )
                    Doctor_create.photo = new_filename
                    if file and allowed_file(file.filename):
                        filename = secure_filename(new_filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], "doctors", filename))
                    db.session.add(Doctor_create)
                    db.session.commit()
                    return redirect(url_for('admin_dash'))
                except Exception as e:
                    flash(f'something wrong', category='danger')
                    print(str(e))
        if add_doctor_form.errors != {}:
            for err_msg in add_doctor_form.errors.values():
                flash(
                    f'there was an error with adding doctor: {err_msg}',
                    category='danger'
                )
    return render_template('add-doctor.html', form=add_doctor_form)


@app.route('/checkout-success', methods=['GET'], strict_slashes=False)
def checkout_success():
    doctor = session.get('doctor', None)
    date = session.get('date', None)
    time = session.get('time', None)

    session.pop('doctor', None)
    session.pop('date', None)
    session.pop('time', None)
    return render_template('booking-success.html', doctor=doctor, date=date, time=time)


@app.route('/checkout', methods=['GET', 'POST'], strict_slashes=False)
def patient_checkout():
    checkout_form = checkoutForm()
    doctor_id = 'doc2'
    date = datetime.now()
    time = datetime.now()
    doctor_data = Doctor.query.filter_by(id=doctor_id).first()
    clinic_data = doctor_data.clinic
    gov = clinic_data.governorate
    if request.method == 'POST':
        patient = Patient.query.filter_by(
            email=checkout_form.email_address.data
        ).first()
        if patient:
            patient_create = patient
        else:
            patient_create = Patient(
                name=checkout_form.firstname.data + ' ' + checkout_form.lastname.data,
                phone=checkout_form.phone.data,
                email=checkout_form.email_address.data
            )
        appointment_create = Appointment(
            date=date.strftime('%Y-%m-%d'),
            time=time.strftime('%H:%M:%S'),
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







                color: #fff;







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







            <div class="logo">



                <img src="cid:logo_image" alt="Your Logo" width="200">



            </div>







            <div class="content">







                <p>Dear {patient_create.name},</p>







                <p>We are writing to confirm your upcoming appointment at {clinic_data.name}.</p>







                <h3>Appointment Details:</h3>







                <ul>







                    <li><strong>Date:</strong> {date.strftime('%d %b %Y')}</li>







                    <li><strong>Time:</strong> {time.strftime("%H:%M:%S")}</li>







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
        db.session.add(patient_create)
        db.session.add(appointment_create)
        db.session.add(message_create)
        db.session.commit()
        session['doctor'] = doctor_data.name
        session['date'] = date.strftime('%d %b %Y')
        session['time'] = time.strftime('%H:%M:%S')
        return redirect(url_for('checkout_success'))
    return render_template(
        'checkout.html',
        doctor=doctor_data,
        clinic=clinic_data,
        gov=gov,
        date=date.strftime('%d %b %Y'),
        form=checkout_form
    )

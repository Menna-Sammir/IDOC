from app import app, db, principal
from flask import render_template, redirect, url_for, flash, request, current_app
from app.models.models import *
from app.views.forms.checkout_form import checkoutForm
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from datetime import datetime
from flask import session




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


# todo special page
@app.route('/specialities', methods=['GET', 'POST'], strict_slashes=False, endpoint='specialities')
def specialities():
    return render_template(
        'specialities.html'
    )

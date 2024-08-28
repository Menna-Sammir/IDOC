from app import app, db, principal
from flask import render_template, redirect, url_for, flash, request, current_app
from app.models.models import User, Clinic, Doctor, Role
from app.views.checkout_form import checkoutForm
from flask_mail import Mail


from datetime import datetime


@app.route('/Booking', methods=['GET', 'POST'])
def Booking():
    if request.method == 'POST':
        # date = request.form.get('date')

        time = request.form.get('time')
        doctor_id = 1
        return redirect(url_for('patient_checkout'))
    return render_template('booking.html')


@app.route('/checkout', methods=['GET', 'POST'])
def patient_checkout():
    checkout_form = checkoutForm()
    doctor_id = 'doc2'
    if request.method == 'POST':
        print('hhhhhorlo')
    date = datetime.now().strftime('%d %b %Y')
    doctor_data = Doctor.query.filter_by(id=doctor_id).first()
    clinic_data = doctor_data.clinic
    gov = clinic_data.governorate
    return render_template('checkout.html', doctor=doctor_data, clinic=clinic_data, gov = gov, date = date, form = checkout_form)


# current_user = request.args.get('current_user', None)
# hhh =

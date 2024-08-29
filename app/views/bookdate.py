from app import app, db
from flask import render_template, request
from flask_principal import Permission, RoleNeed
from app.models.models import *
from datetime import datetime, timedelta
from app.views.calnderdoc import AppointmentForm

admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))

def convert_to_24_hour(time_str):
    return datetime.strptime(time_str, '%I%p').time()

@app.route('/book', methods=['GET', 'POST'])
def doctor_appointments():
    form = AppointmentForm()
    doctor_id = 'd9f2f180-fa4e-4d20-8898-6c40ed7c75a7'
    doctor = Doctor.query.get_or_404(doctor_id)
    clinic = doctor.clinic
    specialization_name = doctor.specialization.specialization_name
    dates = []

    for i in range(6):
        date = datetime.now() + timedelta(days=i)
        dates.append((date.strftime('%Y-%m-%d'), date.strftime('%A')))

    timeslots_by_date = {}

    for date in dates:
        daily_timeslots = []
        for hours in clinic.working_hours.split(','):
            # from 10:00 AM to 12:00 PM
            start_hour, end_hour = map(lambda x: x.strip(), hours.split('-'))
            start_hour_24 = convert_to_24_hour(start_hour)
            end_hour_24 = convert_to_24_hour(end_hour)

            start_hour_int = start_hour_24.hour
            end_hour_int = end_hour_24.hour

            for hour in range(start_hour_int, end_hour_int):
                start_time = datetime.strptime(f"{hour}:00", '%H:%M').time()
                end_time = datetime.strptime(f"{hour + 1}:00", '%H:%M').time()
                timeslot = f"{date[0]} {start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"
                daily_timeslots.append((timeslot, f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"))

        timeslots_by_date[date[0]] = daily_timeslots

    if request.method == 'POST':
        selected_timeslot = request.form['timeslot']
        return redirect(url_for('checkout', doctor_id=doctor.id, timeslot=selected_timeslot))


        new_appointment = Appointment(
            doctor_id=doctor.id,
            date=date,
            time=start_time
        )
        db.session.add(new_appointment)
        db.session.commit()
        return "Appointment booked successfully!"

    return render_template('booking.html', form=form, doctor=doctor, dates=dates, timeslots_by_date=timeslots_by_date, clinic=clinic, specialization_name=specialization_name)

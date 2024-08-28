from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models.models import *
from flask_principal import Permission, RoleNeed
from werkzeug.utils import secure_filename
import uuid
from app.views.forms.addClinic_form import ClinicForm
from app.views.forms.addDoctor_form import DoctorForm
from app import translate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import secrets
import smtplib
import os

admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# admin dashboard page >>> view appointments today
@app.route(
    '/admin_dashboard',
    methods=['GET', 'POST'],
    strict_slashes=False,
    endpoint='dashboard'
)
@login_required
@admin_permission.require(http_exception=403)
def admin_dash():
    doctor_details = db.session.query(Doctor).all()
    clinic_details = db.session.query(Clinic).all()
    doctor_count = db.session.query(Doctor).count()
    clinic_count = db.session.query(Clinic).count()
    patient_count = db.session.query(Patient).count()
    return render_template(
        'admin-dashboard.html',
        doctor_details=doctor_details,
        clinic_details=clinic_details,
        doctor_count=doctor_count,
        clinic_count=clinic_count,
        patient_count=patient_count
    )


@login_required
@admin_permission.require(http_exception=403)
@app.route(
    '/add_clinic', methods=['GET', 'POST'], strict_slashes=False, endpoint='add_clinic'
)
def add_clinic():
    add_clinic_form = ClinicForm()
    govs = Governorate.query.filter().all()
    add_clinic_form.gov_id.choices = [('', translate('Select a governorate'))] + [
        (gov.id, translate(gov.governorate_name)) for gov in govs
    ]
    if request.method == 'POST':
        try:
            clinic = User.query.filter_by(name=add_clinic_form.clinicName.data).first()

            if clinic:
                flash(translate('clinic already exists!'))
            else:
                if add_clinic_form.validate_on_submit():
                    user_to_create = User(
                        name=add_clinic_form.clinicName.data,
                        email=add_clinic_form.email_address.data,
                        activated=False
                    )
                    Clinic_create = Clinic(
                        phone=add_clinic_form.phone.data,
                        address=add_clinic_form.clinicAddress.data,
                        governorate_id=add_clinic_form.gov_id.data,
                        users=user_to_create
                    )
                    clinic_role = Role.query.filter_by(
                        role_name='clinic'
                    ).first_or_404()
                    role_to_create = UserRole(
                        role_id=clinic_role.id, user=user_to_create
                    )

                    if 'logo' not in request.files:
                        flash(translate('No file part'))
                        return redirect(request.url)
                    file = request.files['logo']
                    if file.filename == '':
                        flash(translate('No selected file'))
                        return redirect(request.url)
                    unique_str = str(uuid.uuid4())[:8]
                    original_filename, extension = os.path.splitext(file.filename)
                    new_filename = f"{unique_str}_{add_clinic_form.clinicName.data.replace(' ', '_')}{extension}"
                    user_to_create.photo = new_filename

                    if file and allowed_file(file.filename):
                        filename = secure_filename(new_filename)
                        file.save(
                            os.path.join(
                                app.config['UPLOAD_FOLDER'], 'clinic', filename
                            )
                        )
                    temp_password = secrets.token_urlsafe(8)
                    user_to_create.temp_pass = temp_password
                    db.session.add(user_to_create)
                    db.session.add(role_to_create)
                    db.session.add(Clinic_create)
                    db.session.commit()
                    try:
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        email_address = os.getenv('EMAIL_ADDRESS')
                        app_password = os.getenv('APP_PASSWORD')
                        server.login(email_address, app_password)
                        logo_path = os.path.join(
                            app.root_path, 'static', 'img', 'logo.png'
                        )
                        msg = MIMEMultipart()
                        msg['From'] = email_address
                        msg['To'] = add_clinic_form.email_address.data
                        msg['Subject'] = 'IDOC, Email confirmation'
                        reset_link = url_for(
                            'reset_password',
                            email=add_clinic_form.email_address.data,
                            _external=True
                        )
                        message_body = f"Your temporary password is: {temp_password}\n\nUse this link to reset your password:<a href=' {reset_link}'>click Here</a>"

                        message = message_body
                        msg.attach(MIMEText(message, 'html'))
                        with open(logo_path, 'rb') as f:
                            logo_data = f.read()
                        logo_part = MIMEImage(logo_data)
                        logo_part.add_header('Content-ID', '<logo_image>')
                        msg.attach(logo_part)

                        server.send_message(msg)
                        server.quit()
                        # flash('A temporary password has been sent to your email.', 'success')
                    except Exception as e:
                        flash(f'something wrong', category='danger')
                        print(str(e))
                    flash(
                        f'added clinic success  ${user_to_create.name}',
                        category='success'
                    )
                    return redirect(url_for('dashboard'))
                if add_clinic_form.errors != {}:
                    for err_msg in add_clinic_form.errors.values():
                        print('error', err_msg)
                        flash(
                            f'there was an error with creating a user: {err_msg}',
                            category='danger'
                        )
        except Exception as e:
            flash(f'something wrong', category='danger')
            print('Exception', e)
    return render_template('add-clinic.html', form=add_clinic_form)


@login_required
# @clinic_permission.require(http_exception=403)
@app.route(
    '/add_doctor', methods=['GET', 'POST'], strict_slashes=False, endpoint='add_doctor'
)
def add_doctor():
    add_doctor_form = DoctorForm()
    specializations = Specialization.query.filter().all()

    add_doctor_form.specialization_id.choices = [
        ('', translate('Select a specialization'))
    ] + [
        (specialization.id, translate(specialization.specialization_name))
        for specialization in specializations
    ]
    if request.method == 'POST':
        if add_doctor_form.validate_on_submit():
            doctor_name = (
                add_doctor_form.firstname.data + ' ' + add_doctor_form.lastname.data
            )
            try:
                if current_user.user_roles.role.role_name == 'clinic':
                    clinic = Clinic.query.filter_by(user_id=current_user.id).first_or_404()
                    doc_dur = int(add_doctor_form.duration.data)
                    user_to_create = User(
                        name=doctor_name,
                        email=add_doctor_form.email_address.data,
                        activated=False
                    )
                    Doctor_create = Doctor(
                        phone=add_doctor_form.phone.data,
                        From_working_hours=add_doctor_form.fromHour.data,
                        To_working_hours=add_doctor_form.toHour.data,
                        duration=str(doc_dur * 100),
                        price=add_doctor_form.price.data,
                        specialization_id=add_doctor_form.specialization_id.data,
                        isAdv = False,
                        clinic_id=clinic.id,
                        iDNum=add_doctor_form.IDNum.data,
                        users = user_to_create
                    )
                    if 'photo' not in request.files:
                        flash(translate('No file part'))
                        return redirect(request.url)
                    file = request.files['photo']
                    if file.filename == '':
                        flash(translate('No selected file'))
                        return redirect(request.url)
                    unique_str = str(uuid.uuid4())[:8]
                    original_filename, extension = os.path.splitext(file.filename)
                    new_filename = f"{unique_str}_{current_user.name.replace(' ', '_')}_{doctor_name.replace(' ', '_')}{extension}"
                    user_to_create.photo = new_filename
                    if file and allowed_file(file.filename):
                        filename = secure_filename(new_filename)
                        file.save(
                            os.path.join(
                                app.config['UPLOAD_FOLDER'], 'doctors', filename
                            )
                        )
                    doctor_role = Role.query.filter_by(
                        role_name='doctor'
                    ).first_or_404()
                    role_to_create = UserRole(
                        role_id=doctor_role.id, user=user_to_create
                    )
                    temp_password = secrets.token_urlsafe(8)
                    user_to_create.temp_pass = temp_password
                    db.session.add(user_to_create)
                    db.session.add(role_to_create)
                    db.session.add(Doctor_create)
                    db.session.commit()
                    try:
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        email_address = os.getenv('EMAIL_ADDRESS')
                        app_password = os.getenv('APP_PASSWORD')
                        server.login(email_address, app_password)
                        logo_path = os.path.join(
                            app.root_path, 'static', 'img', 'logo.png'
                        )
                        msg = MIMEMultipart()
                        msg['From'] = email_address
                        msg['To'] = add_doctor_form.email_address.data
                        msg['Subject'] = 'IDOC, Email confirmation'
                        reset_link = url_for(
                            'reset_password',
                            email=add_doctor_form.email_address.data,
                            _external=True
                        )
                        message_body = f"Your ID is: {add_doctor_form.IDNum.data} temporary password is: {temp_password}\n\nUse this link to reset your password:<a href=' {reset_link}'>click Here</a>"

                        message = message_body
                        msg.attach(MIMEText(message, 'html'))
                        with open(logo_path, 'rb') as f:
                            logo_data = f.read()
                        logo_part = MIMEImage(logo_data)
                        logo_part.add_header('Content-ID', '<logo_image>')
                        msg.attach(logo_part)

                        server.send_message(msg)
                        server.quit()
                        # flash('A temporary password has been sent to your email.', 'success')
                    except Exception as e:
                        flash(f'something wrong', category='danger')
                        print(str(e))
                    flash(
                        f'added Doctor success created with ID ${Doctor_create.iDNum}',
                        category='success'
                    )
                    return redirect(url_for('clinic_dash'))
            except Exception as e:
                print(str(e))
                flash(f'something wrong', category='danger')
        if add_doctor_form.errors != {}:
            for err_msg in add_doctor_form.errors.values():
                flash(
                    f'there was an error with adding doctor: {err_msg}',
                    category='danger'
                )
    return render_template('add-doctor.html', form=add_doctor_form)

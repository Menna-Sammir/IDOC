from app import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from datetime import datetime
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from flask_login import login_required, current_user
from flask import session
from datetime import date
from app.models.models import Specialization, User, Doctor,  Patient, Appointment, Clinic, Message,  Governorate, Role
from flask_principal import Permission, RoleNeed, Identity, AnonymousIdentity, identity_loaded, identity_changed

admin_permission = Permission(RoleNeed('Admin'))
doctor_permission = Permission(RoleNeed('doctor'))
clinic_permission = Permission(RoleNeed('clinic'))


# admin dashboard page >>> view appointments today
# @app.route('/admin_dashboard', methods=['GET', 'POST'])
# @login_required
# def admin_dash():
#     user_id = request.args.get('current_user', None)
    
#     user = User.query.filter_by(id=user_id).first()

#     doctor_id = user.doctor_id

#     doctor = Doctor.query.filter_by(id=doctor_id).first()

 
#     # if request.method == 'POST':
#     #     return redirect(url_for('logout'))

#     return render_template('admin-dashboard.html')



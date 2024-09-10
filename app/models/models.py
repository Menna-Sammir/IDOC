from app import db, login_manager, app, bcrypt, translate
from app.models.base import BaseModel
from sqlalchemy.dialects.mysql import (
    VARCHAR,
    INTEGER,
    BOOLEAN,
    DATE,
    TIME,
    TEXT,
    DATETIME
)
import logging
from sqlalchemy import ForeignKey, func, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from flask_login import UserMixin, current_user
from flask_principal import RoleNeed, identity_loaded, UserNeed
from sqlalchemy import func
from datetime import date, datetime, timedelta
from app.models.notiTime import calculate_time_ago
from flask import g
from enum import Enum


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    if hasattr(current_user, 'user_roles'):
        identity.provides.add(RoleNeed(current_user.user_roles.role.role_name))


@app.context_processor
def inject_cache_id():
    return {'cache_id': app.config['CACHE_ID']}


@app.before_request
def load_notification():
    current_time = datetime.now()
    if current_user.is_authenticated and hasattr(current_user.clinic, 'id'):
        notification = Notification.query.filter_by(clinic_id=current_user.clinic.id)
        processed_notifications = [
            {
                # 'doctor': n.appointment.doctor.name,
                # 'patient': n.appointment.patient.name,
                'body': n.noteBody,
                'isRead': n.isRead,
                'time': n.time.strftime('%H:%M %p'),
                'date': n.date.strftime('%d %B'),
                # 'photo': n.appointment.doctor.photo,
                'formatted_time': calculate_time_ago(current_time, n.notDate)
            }
            for n in notification.all()[:10]
        ]
        g.notifications = processed_notifications
        g.notification_count = len(notification.filter_by(isRead=False).all()) | 0


@app.context_processor
def inject_notification():
    return dict(
        notifications=g.get('notifications', ''),
        notification_count=g.get('notification_count', 0)
    )


class AppStatus(Enum):
    Pending = "Pending"
    Confirmed = "Confirmed"
    Cancelled = "Cancelled"
    Completed = "Completed"


class PatientHisType(Enum):
    Lab = "Lab"
    X_ray = "X-ray"


class MedicineTime(Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    EVENING = "Evening"
    NIGHT = "Night"


class BloodGroup(Enum):
    A_positive = 'A+'
    A_negative = 'A-'
    B_positive = 'B+'
    B_negative = 'B-'
    AB_positive = 'AB+'
    AB_negative = 'AB-'
    O_positive = 'O+'
    O_negative = 'O-'


class Allergy(Enum):
    No_Allergy = 'No Allergy'
    Peanuts = 'Peanuts'
    Shellfish = 'Shellfish'
    Dairy = 'Dairy'
    Eggs = 'Eggs'
    Wheat = 'Wheat'
    Soy = 'Soy'
    Tree_nuts = 'Tree Nuts'
    Fish = 'Fish'
    Latex = 'Latex'
    Pollen = 'Pollen'
    Dust_mites = 'Dust Mites'
    Insect_stings = 'Insect Stings'
    Mold = 'Mold'
    Pet_dander = 'Pet Dander'
    Medications = 'Medications'
    Gluten = 'Gluten'
    Perfumes_and_scents = 'Perfumes and Scents'
    Sunlight = 'Sunlight'
    Cold_temperatures = 'Cold Temperatures'
    Nickel = 'Nickel'
    Sulfites = 'Sulfites'
    Red_meat = 'Red Meat'


class Specialization(BaseModel):
    __tablename__ = 'specialization'

    specialization_name = db.Column(VARCHAR(100), nullable=False)
    photo = db.Column(VARCHAR(255))
    doctors = relationship('Doctor', back_populates='specialization')


class Doctor(BaseModel):
    __tablename__ = 'doctor'

    phone = db.Column(VARCHAR(50), nullable=False)
    price = db.Column(INTEGER)
    duration = db.Column(TIME)
    isAdv = db.Column(BOOLEAN, nullable=False)
    iDNum = db.Column(VARCHAR(50), nullable=False, unique=True)

    specialization_id = db.Column(
        VARCHAR(60), ForeignKey('specialization.id'), nullable=False
    )
    clinic_id = db.Column(VARCHAR(36), ForeignKey('clinic.id'), nullable=True)
    From_working_hours = db.Column(TIME(), nullable=False)
    To_working_hours = db.Column(TIME(), nullable=False)

    user_id = db.Column(
        VARCHAR(60), ForeignKey('users.id'), nullable=False, unique=True
    )
    users = relationship('User', back_populates='doctor', lazy='joined')

    specialization = relationship('Specialization', back_populates='doctors')
    clinic = relationship('Clinic', back_populates='doctors')
    appointments = relationship('Appointment', back_populates='doctor')

    def total_earnings(self):
        appointment_count = (
            db.session.query(func.count(Appointment.id))
            .filter(Appointment.doctor_id == self.id)
            .scalar()
            or 0
        )
        return translate(appointment_count * (self.price or 0))


class Clinic(BaseModel):
    __tablename__ = 'clinic'

    phone = db.Column(VARCHAR(50), nullable=False)
    address = db.Column(VARCHAR(255), nullable=False)
    governorate_id = db.Column(
        VARCHAR(60), ForeignKey('governorate.id'), nullable=False
    )

    user_id = db.Column(
        VARCHAR(60), ForeignKey('users.id'), nullable=False, unique=True
    )
    users = relationship('User', back_populates='clinic')

    governorate = relationship('Governorate', back_populates='clinics')
    doctors = relationship('Doctor', back_populates='clinic')
    appointments = relationship('Appointment', back_populates='clinic')
    notifications = relationship('Notification', back_populates='clinic')

    def total_earnings(self):
        today = date.today()
        total_earnings = 0
        for doctor in self.doctors:
            appointment_count = (
                db.session.query(func.count(Appointment.id))
                .filter(
                    Appointment.clinic_id == self.id,
                    Appointment.doctor_id == doctor.id,
                    func.date(Appointment.date) == today
                )
                .scalar()
                or 0
            )
            total_earnings += appointment_count * (doctor.price or 0)
        return total_earnings

    def doctor_count(self):
        return len(self.doctors)


class Governorate(BaseModel):
    __tablename__ = 'governorate'

    governorate_name = db.Column(VARCHAR(100), nullable=False)
    clinics = relationship('Clinic', back_populates='governorate')
    patients = relationship('Patient', back_populates='governorate')


class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    name = db.Column(VARCHAR(100), nullable=False)
    email = db.Column(VARCHAR(100), nullable=False)
    password = db.Column(VARCHAR(255), nullable=True)
    photo = db.Column(VARCHAR(255), nullable=True)
    activated = db.Column(BOOLEAN, nullable=False)
    temp_password = db.Column(VARCHAR(200), nullable=True)

    doctor = relationship('Doctor', back_populates='users')
    patient = relationship('Patient', back_populates='users')
    clinic = relationship('Clinic', back_populates='users', uselist=False)
    user_roles = relationship('UserRole', uselist=False, back_populates='user')
    patient_history = relationship('PatientHistory', back_populates='user')
    patient_medicine = relationship('PatientMedicine', back_populates='user')

    @property
    def password_hash(self):
        return self.password_hash

    @password_hash.setter
    def password_hash(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode(
            'utf-8'
        )

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    @property
    def temp_pass(self):
        return self.temp_pass

    @temp_pass.setter
    def temp_pass(self, plain_text_password):
        self.temp_password = bcrypt.generate_password_hash(plain_text_password).decode(
            'utf-8'
        )

    def temp_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.temp_password, attempted_password)


class UserRole(BaseModel):
    __tablename__ = 'user_roles'

    user_id = db.Column(VARCHAR(60), ForeignKey('users.id'), nullable=False)
    role_id = db.Column(VARCHAR(60), ForeignKey('roles.id'), nullable=False)

    user = relationship('User', back_populates='user_roles')
    role = relationship('Role', back_populates='user_roles')


class Role(BaseModel):
    __tablename__ = 'roles'
    role_name = db.Column(VARCHAR(100), unique=True, nullable=False)
    user_roles = relationship('UserRole', uselist=False, back_populates='role')


class Patient(BaseModel):
    __tablename__ = 'patient'

    phone = db.Column(VARCHAR(50), nullable=False)

    user_id = db.Column(
        VARCHAR(60), ForeignKey('users.id'), nullable=False, unique=True
    )
    users = relationship('User', back_populates='patient')

    governorate_id = db.Column(VARCHAR(60), ForeignKey('governorate.id'), nullable=True)
    governorate = relationship('Governorate', back_populates='patients')

    age = db.Column(INTEGER, nullable=True)
    address = db.Column(VARCHAR(255), nullable=True)

    allergy = db.Column(SQLAlchemyEnum(Allergy), nullable=True)
    blood_group = db.Column(SQLAlchemyEnum(BloodGroup), nullable=True)

    histories = db.relationship('PatientHistory', backref='patient', uselist=False)
    medicine = db.relationship('PatientMedicine', backref='patient', uselist=False)
    appointments = db.relationship('Appointment', back_populates='patient')

class MedicineTimes(BaseModel):
    __tablename__ = 'MedicineTimes'

    medicine_id = db.Column(VARCHAR(60), ForeignKey('PatientMedicine.id'), nullable=False)
    time_of_day = db.Column(SQLAlchemyEnum(MedicineTime), nullable=False)

    patient_medicine = relationship("PatientMedicine", back_populates='medicine_times')


class PatientMedicine(BaseModel):
    __tablename__ = 'PatientMedicine'

    medName = db.Column(VARCHAR(255), nullable=False)
    Quantity = db.Column(VARCHAR(255), nullable=False)
    Date = db.Column(DATE, nullable=False)
    patient_id = db.Column(VARCHAR(60), ForeignKey('patient.id'), nullable=False)
    Added_By = db.Column(VARCHAR(60), ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='patient_medicine')
    medicine_times = relationship("MedicineTimes", back_populates='patient_medicine', uselist=True)




class PatientHistory(BaseModel):
    __tablename__ = 'PatientHistory'
    details = db.Column(VARCHAR(255), nullable=False)
    type =  db.Column(SQLAlchemyEnum(PatientHisType), nullable=True)
    addedBy = db.Column(VARCHAR(60), ForeignKey('users.id'), nullable=False, unique=True)
    patient_id = db.Column(VARCHAR(60), ForeignKey('patient.id'), unique=True)

    user = db.relationship('User', back_populates='patient_history')



class Appointment(BaseModel):
    __tablename__ = 'appointment'

    date = db.Column(DATE, nullable=False)
    time = db.Column(TIME, nullable=False)
    seen = db.Column(BOOLEAN, nullable=False)
    rates = db.Column(INTEGER, nullable=True)
    comment = db.Column(VARCHAR(50), nullable=True)
    Report = db.Column(VARCHAR(255), nullable=True)
    Diagnosis = db.Column(VARCHAR(255), nullable=True)
    status = db.Column(SQLAlchemyEnum(AppStatus), nullable=False)
    follow_up = db.Column(DATETIME, nullable=True)

    clinic_id = db.Column(VARCHAR(60), ForeignKey('clinic.id'), nullable=False)
    patient_id = db.Column(VARCHAR(60), ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(VARCHAR(60), ForeignKey('doctor.id'), nullable=False)
    clinic = relationship('Clinic', back_populates='appointments')
    patient = relationship('Patient', back_populates='appointments')
    doctor = relationship('Doctor', back_populates='appointments', lazy='joined')
    messages = relationship('Message', uselist=False, back_populates='appointment')
    notifications = relationship(
        'Notification', uselist=False, back_populates='appointment'
    )
    @property
    def time_range(self):
        appointment_end_time = (datetime.combine(date.today(), self.time) + timedelta(hours=1)).time()
        return f"{self.time.strftime('%H:%M')} - {appointment_end_time.strftime('%H:%M')}"

    @property
    def formatted_date(self):
        return self.date.strftime('%A, %d %B').capitalize()

    @property
    def followup_date(self):
        if self.follow_up:
            return self.follow_up.strftime('%A, %d %B').capitalize()
        else:
            return "N/A"


    def status_bg(self):
        if self.status == AppStatus.Pending.value:
            return "bg-info"
        elif self.status == AppStatus.Confirmed.value:
            return "bg-success"
        elif self.status == AppStatus.Cancelled.value:
            return "bg-danger"
        elif self.status == AppStatus.Completed.value:
            return "bg-secondary"
        else:
            return "bg-secondary"


class Message(BaseModel):
    __tablename__ = 'message'

    message_body = db.Column(TEXT, nullable=True)
    status = db.Column(BOOLEAN, nullable=False)

    appointment_id = db.Column(
        VARCHAR(60), ForeignKey('appointment.id'), nullable=False, unique=True
    )
    appointment = relationship('Appointment', back_populates='messages')


class Notification(BaseModel):
    __tablename__ = 'notification'
    noteBody = db.Column(TEXT, nullable=False)
    isRead = db.Column(BOOLEAN, nullable=False)
    time = db.Column(TIME, nullable=False, default=func.now())
    date = db.Column(DATE, nullable=False, default=func.now())
    notDate = db.Column(DATETIME, nullable=False, default=func.now())

    clinic_id = db.Column(VARCHAR(60), ForeignKey('clinic.id'), nullable=False)
    appointment_id = db.Column(
        VARCHAR(60), ForeignKey('appointment.id'), nullable=False, unique=True
    )

    clinic = relationship('Clinic', back_populates='notifications')
    appointment = relationship('Appointment', back_populates='notifications')

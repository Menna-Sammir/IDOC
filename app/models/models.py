from app import db, login_manager,app
from app.models.base import BaseModel
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, BOOLEAN, DATE, TIME, TEXT
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship
from app import bcrypt
from flask_login import UserMixin
from datetime import datetime
from flask_principal import RoleNeed, identity_loaded, UserNeed
from flask_login import current_user
from sqlalchemy import func
from datetime import date

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    if hasattr(current_user, 'roles'):
        identity.provides.add(RoleNeed(current_user.roles.role_name))

@app.context_processor
def inject_cache_id():
    return {'cache_id': app.config['CACHE_ID']}


class Specialization(BaseModel):
    __tablename__ = 'specialization'

    specialization_name = db.Column(VARCHAR(100), nullable=False)
    photo = db.Column(VARCHAR(255))
    doctors = relationship("Doctor", back_populates="specialization")

class Doctor(BaseModel):
    __tablename__ = 'doctor'

    name = db.Column(VARCHAR(100), nullable=False)
    phone = db.Column(VARCHAR(50), nullable=False)
    email = db.Column(VARCHAR(100), nullable=False)
    photo = db.Column(VARCHAR(255))
    price = db.Column(INTEGER)

    specialization_id = db.Column(VARCHAR(60), ForeignKey('specialization.id'), nullable=False)
    clinic_id = db.Column(VARCHAR(36), ForeignKey('clinic.id'), nullable=True)

    users = db.relationship('User', backref='doctor', uselist=False)
    specialization = relationship("Specialization", back_populates="doctors")
    clinic = relationship("Clinic", back_populates="doctors")
    appointments = relationship("Appointment", back_populates="doctor")
    
    def total_earnings(self):
        appointment_count = db.session.query(func.count(Appointment.id)).filter(Appointment.doctor_id == self.id).scalar() or 0
        return appointment_count * (self.price or 0)

class Clinic(BaseModel):
    __tablename__ = 'clinic'

    name = db.Column(VARCHAR(100), nullable=False)
    phone = db.Column(VARCHAR(50), nullable=False)
    email = db.Column(VARCHAR(100), nullable=False)
    address = db.Column(VARCHAR(255), nullable=False)
    working_hours = db.Column(VARCHAR(50), nullable=False)
    photo = db.Column(VARCHAR(255))

    governorate_id = db.Column(VARCHAR(60), ForeignKey('governorate.id'), nullable=False)
    users = db.relationship('User', backref='clinic', uselist=False)
    governorate = relationship("Governorate", back_populates="clinics")
    doctors = relationship("Doctor", back_populates="clinic")
    appointments = relationship("Appointment", back_populates="clinic")

    def total_earnings(self):
        today = date.today()
        total_earnings = 0
        for doctor in self.doctors:
            appointment_count = db.session.query(func.count(Appointment.id)).filter(
                Appointment.clinic_id == self.id,
                Appointment.doctor_id == doctor.id,
                func.date(Appointment.date) == today
            ).scalar() or 0
            total_earnings += appointment_count * (doctor.price or 0)
        return total_earnings


    def doctor_count(self):
        return len(self.doctors)

class Governorate(BaseModel):
    __tablename__ = 'governorate'

    governorate_name = db.Column(VARCHAR(100), nullable=False)
    clinics = relationship("Clinic", back_populates="governorate")

class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    name = db.Column(VARCHAR(100), nullable=False)
    email = db.Column(VARCHAR(100), nullable=False)
    password = db.Column(VARCHAR(255), nullable=False)
    photo = db.Column(VARCHAR(255), nullable=True)

    doctor_id = db.Column(VARCHAR(60), ForeignKey('doctor.id'), unique=True)
    clinic_id = db.Column(VARCHAR(60), ForeignKey('clinic.id'), unique=True)
    roles = relationship("Role", uselist=False, back_populates="user")

    @property
    def password_hash(self):
        return self.password_hash

    @password_hash.setter
    def password_hash(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)



class Role(BaseModel):
    __tablename__ = 'roles'

    user_id = db.Column(VARCHAR(60), ForeignKey('user.id'), nullable=False, unique=True)
    role_name = db.Column(VARCHAR(100), nullable=False)
    user = relationship("User", back_populates="roles")

class Patient(BaseModel):
    __tablename__ = 'patient'
    name = db.Column(VARCHAR(100), nullable=False)
    phone = db.Column(VARCHAR(50), nullable=False)
    email = db.Column(VARCHAR(100), nullable=False)
    # photo = db.Column(db.String(255))

    appointments = relationship("Appointment", back_populates="patient")

class Appointment(BaseModel):
    __tablename__ = 'appointment'

    date = db.Column(DATE, nullable=False)
    time = db.Column(TIME, nullable=False)
    status = db.Column(BOOLEAN, nullable=False)
    seen = db.Column(BOOLEAN, nullable=False)

    clinic_id = db.Column(VARCHAR(60), ForeignKey('clinic.id'), nullable=False)
    patient_id = db.Column(VARCHAR(60), ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(VARCHAR(60), ForeignKey('doctor.id'), nullable=False)
    clinic = relationship("Clinic", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    messages = relationship("Message", uselist=False, back_populates="appointment")

class Message(BaseModel):
    __tablename__ = 'message'

    message_body = db.Column(TEXT, nullable=False)
    status = db.Column(BOOLEAN, nullable=False)

    appointment_id = db.Column(VARCHAR(60), ForeignKey('appointment.id'), nullable=False, unique=True)
    appointment = relationship("Appointment", back_populates="messages")

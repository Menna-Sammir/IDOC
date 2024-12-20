import unittest
from app import app, db
from flask_login import login_user
from app.models.models import User, Appointment, Clinic, Governorate, Doctor, Patient, Specialization, Role, UserRole

class TestCancelAppointment(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        app.config['WTF_CSRF_ENABLED'] = False

        db.create_all()

        self.connection = db.engine.connect()
        self.transaction = self.connection.begin()

        options = dict(bind=self.connection, binds={})
        self.session = db.create_scoped_session(options=options)
        db.session = self.session

        self.role = self.create_test_role()
        self.user = self.create_test_user()
        self.governorate = self.create_test_governorate()
        self.clinic = self.create_test_clinic()
        self.specialization = self.create_test_specialization()
        self.doctor = self.create_test_doctor()
        self.patient = self.create_test_patient()
        self.appointment = self.create_test_appointment()

    def tearDown(self):
        self.transaction.rollback()
        self.connection.close()
        self.app_context.pop()

    def create_test_role(self):
        role = Role.query.filter_by(role_name='Patient').first()
        if not role:
            role = Role(role_name='Patient')
            self.session.add(role)
            self.session.commit()
        return role

    def create_test_user(self):
        user = User(
            name='Test User', 
            email='testuser@example.com', 
            password='password',
            activated=True
        )
        self.session.add(user)
        self.session.commit()

        user_role = UserRole(user_id=user.id, role_id=self.role.id)
        self.session.add(user_role)
        self.session.commit()

        return user

    def create_test_governorate(self):
        governorate = Governorate(governorate_name='Test Governorate')
        self.session.add(governorate)
        self.session.commit()
        return governorate

    def create_test_clinic(self):
        clinic = Clinic(
            phone='0123456789', 
            address='Test Address', 
            governorate_id=self.governorate.id, 
            user_id=self.user.id
        )
        self.session.add(clinic)
        self.session.commit()
        return clinic

    def create_test_specialization(self):
        specialization = Specialization(
            specialization_name='Test Specialization', 
            photo='test_photo.png'
        )
        self.session.add(specialization)
        self.session.commit()
        return specialization

    def create_test_doctor(self):
        doctor = Doctor(
            phone='0123456789',
            price=200,
            duration='01:00:00',
            isAdv=False,
            iDNum='12345',
            specialization_id=self.specialization.id,
            clinic_id=self.clinic.id,
            From_working_hours='09:00:00',
            To_working_hours='17:00:00',
            user_id=self.user.id
        )
        self.session.add(doctor)
        self.session.commit()
        return doctor

    def create_test_patient(self):
        patient = Patient(
            phone='0123456789',
            user_id=self.user.id,
            governorate_id=self.governorate.id
        )
        self.session.add(patient)
        self.session.commit()
        return patient

    def create_test_appointment(self):
        appointment = Appointment(
            clinic_id=self.clinic.id,
            patient_id=self.patient.id,
            doctor_id=self.doctor.id,
            date='2024-09-30',
            time='10:00:00',
            seen=False,
            status='Pending'
        )
        self.session.add(appointment)
        self.session.commit()
        return appointment

    def test_cancel_appointment(self):
        with self.app as client:
            with client.session_transaction() as session:
                session['_user_id'] = str(self.user.id)  

            data = {'appointment_id': str(self.appointment.id)}
            result = client.post('/cancel_appointment', data=data, follow_redirects=True)

            self.assertEqual(result.status_code, 200)

            self.assertIn(b'Appointment cancelled successfully', result.data)


if __name__ == '__main__':
    unittest.main()

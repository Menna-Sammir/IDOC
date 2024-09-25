import unittest
from app import app, db
from app.models.models import User, Doctor, Clinic, Governorate, Specialization

class TestPatientCheckout(unittest.TestCase):
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

        self.user = self.create_test_user()
        self.governorate = self.create_test_governorate()
        self.clinic = self.create_test_clinic()
        self.specialization = self.create_test_specialization()
        self.doctor = self.create_test_doctor()

    def tearDown(self):
        self.transaction.rollback()
        self.connection.close()
        self.app_context.pop()

    def create_test_user(self):
        user = User(
            name='Test User', 
            email='testuser@example.com', 
            password='password',
            activated=True
        )
        self.session.add(user)
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

    def test_patient_checkout_get(self):
        with self.app.session_transaction() as sess:
            sess['doctor_id'] = self.doctor.id
            sess['date'] = '2024-09-20'
            sess['start_time'] = '09:00 AM'
            sess['end_time'] = '10:00 AM'

        with self.app:
            result = self.app.get('/checkout')
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'Checkout', result.data) 


if __name__ == '__main__':
    unittest.main()

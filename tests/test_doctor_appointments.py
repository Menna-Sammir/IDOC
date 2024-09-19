import unittest
from app import app
from flask_login import login_user
from app.models.models import User, Doctor

class TestDoctorAppointments(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_doctor_appointments_get(self):
        with self.app:
            result = self.app.get('/book?doctor_id=1')
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'Appointment Details', result.data)

if __name__ == '__main__':
    unittest.main()

# Fix bug in doctor appointment test case

# Improve error handling in doctor appointment test

# Add more assertions for doctor appointment

# Refactor doctor appointment test function

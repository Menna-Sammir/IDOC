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

# Improve doctor appointment test coverage

# Adjust mock data for doctor appointment

# Fix typo in doctor_id variable

# Change appointment ID in doctor appointment test

# Add logging for debugging doctor appointment

# Remove unused imports in doctor appointment test

# Update test client setup for doctor appointment

# Fix HTTP status code check in doctor appointment test

# Enhance test reliability for doctor appointment

# Improve performance of doctor appointment test

# Fix flaky doctor appointment test issue

# Modify test for new doctor appointment endpoint

# Adjust test for new doctor appointment schema

# Improve exception handling in doctor appointment test

# Add teardown step for cleanup in doctor appointment test

# Enhance setup logic for doctor appointment test

# Add more test cases for doctor appointment

# Update dependencies for doctor appointment tests

# Reorganize doctor appointment test structure

# Cleanup test data for doctor appointment

# Add mock server responses for doctor appointment

# Handle edge cases in doctor appointment test

# Fix timeout issues in doctor appointment test

# Refactor doctor appointment test setup logic

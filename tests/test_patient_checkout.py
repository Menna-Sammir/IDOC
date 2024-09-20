import unittest
from app import app

class TestPatientCheckout(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_patient_checkout_get(self):
        with self.app:
            result = self.app.get('/checkout')
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'Appointment Confirmation', result.data)

if __name__ == '__main__':
    unittest.main()

# Fix patient checkout route test issue

# Improve patient checkout error handling

# Add more assertions for patient checkout

# Refactor patient checkout test function

# Improve test coverage for patient checkout

# Adjust mock data for patient checkout test

# Fix typo in checkout variable

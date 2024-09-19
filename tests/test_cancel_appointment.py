import unittest
from app import app

class TestCancelAppointment(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_cancel_appointment(self):
        with self.app:
            data = {'appointment_id': '1'}
            result = self.app.post('/cancel_appointment', data=data)
            self.assertEqual(result.status_code, 302)
            self.assertIn(b'Appointment cancelled successfully', result.data)

if __name__ == '__main__':
    unittest.main()

# Fix bug in test case

# Improve error handling

# Add more assertions

# Refactor test function

# Improve test coverage

# Adjust mock data

# Fix typo in variable name

# Change appointment ID in test

# Add logging for debugging

# Remove unused imports

# Update test client setup

# Fix HTTP status code check

# Enhance test reliability

# Improve performance of test

# Fix flaky test issue

# Modify test for new endpoint

# Adjust test for new schema

# Improve exception handling

# Add teardown step for cleanup

# Enhance setup logic for test

# Add more test cases

# Update dependencies for tests

# Reorganize test structure

# Cleanup test data

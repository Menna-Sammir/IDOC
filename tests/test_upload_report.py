import unittest
from app import app
from flask_login import login_user
from app.models.models import User

class TestUploadReport(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_upload_report(self):
        with self.app:
            user = User.query.get(1)
            login_user(user)
            data = {
                'patient_id': '1',
                'appointment_id': '1',
                'diagnosis': 'Test Diagnosis',
                'file': (open('testfile.pdf', 'rb'), 'testfile.pdf')
            }
            result = self.app.post('/upload_report', data=data)
            self.assertEqual(result.status_code, 302)
            self.assertIn(b'Report uploaded successfully', result.data)

if __name__ == '__main__':
    unittest.main()

# Fix upload report route test issue

# Improve upload report error handling

# Add more assertions for upload report

# Refactor upload report test function

# Improve test coverage for upload report

# Adjust mock data for upload report test

# Fix typo in upload report variables

# Change response content check in upload report test

# Add logging for debugging upload report

# Remove unused imports in upload report test

# Update test client setup for upload report

# Fix HTTP status code check in upload report test

# Enhance test reliability for upload report

# Improve performance of upload report test

# Fix flaky upload report test issue

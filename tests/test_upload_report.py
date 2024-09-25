import unittest
from app import app, db
from app.models.models import User, Appointment, Clinic
from flask import url_for

class TestUploadReport(unittest.TestCase):

    def setUp(self):
        # Set up the application for testing
        app.debug = True  
        self.app = app.test_client()
        self.app.testing = True

        # Create the database tables and add a test user
        db.create_all()
        self.user = User(name='Test User', email='test@example.com', password='password', activated=True)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        # Clean up the database after each test
        db.session.remove()
        db.drop_all()

    def login(self):
        # Perform login for testing purposes
        response = self.app.post('/login', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        print("Login response status code:", response.status_code)
        print("Login response data:", response.data)
        return response

    def test_upload_report(self):
        # Check if the main page is reachable
        response = self.app.get('/')
        print("Main page response data:", response.data)

        # Log in before testing report upload
        login_response = self.login()

        # Test uploading a report
        response = self.app.post('/upload_report', data=dict(
            report='Test Report',
            appointment_id=1
        ), follow_redirects=True)

        # Check if the upload was successful
        print("Upload report response status code:", response.status_code)
        print("Upload report response data:", response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Report uploaded successfully', response.data)

if __name__ == '__main__':
    unittest.main()

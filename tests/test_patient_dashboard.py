import unittest
from app import app, db
from flask_login import login_user
from app.models.models import User, Role, UserRole, Patient

class TestPatientDashboard(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

        self.connection = db.engine.connect()
        self.transaction = self.connection.begin()

        options = dict(bind=self.connection, binds={})
        self.session = db.create_scoped_session(options=options)
        db.session = self.session

        self.user = self.create_test_user_with_role()

    def tearDown(self):
        self.transaction.rollback()
        self.connection.close()
        self.app_context.pop()

    def create_test_user_with_role(self):
        role = Role.query.filter_by(role_name='Patient').first()
        if not role:
            role = Role(role_name='Patient')
            self.session.add(role)
            self.session.commit()

        user = User(
            name='Test Patient', 
            email='testpatient@example.com', 
            password='password',
            activated=True
        )
        self.session.add(user)
        self.session.commit()

        user_role = UserRole(user_id=user.id, role_id=role.id)
        self.session.add(user_role)
        self.session.commit()

        patient = Patient(user_id=user.id, phone='0123456789')
        self.session.add(patient)
        self.session.commit()

        return user

    def test_patient_dashboard_get(self):
        with self.app as client:
            with client.session_transaction() as session:
                session['_user_id'] = str(self.user.id)  
    
            result = client.get('/patient_dashboard', follow_redirects=True)
            
            self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()

# Fix patient dashboard route test issue

# Improve patient dashboard error handling

# Add more assertions for patient dashboard

# Refactor patient dashboard test function

# Improve test coverage for patient dashboard

# Adjust mock data for patient dashboard test

# Fix typo in patient dashboard test

# Change response content check in patient dashboard test

# Add logging for debugging patient dashboard

# Remove unused imports in patient dashboard test

# Update test client setup for patient dashboard

# Fix HTTP status code check in patient dashboard test

# Enhance test reliability for patient dashboard

# Improve performance of patient dashboard test

# Fix flaky patient dashboard test issue

# Modify test for new patient dashboard endpoint

# Adjust test for new patient dashboard schema

# Improve exception handling in patient dashboard test

# Add teardown step for cleanup in patient dashboard test

# Enhance setup logic for patient dashboard test

# Add more test cases for patient dashboard

# Update dependencies for patient dashboard tests

# Reorganize patient dashboard test structure

# Cleanup test data for patient dashboard

# Add mock server responses for patient dashboard

# Handle edge cases in patient dashboard test

# Fix timeout issues in patient dashboard test

# Refactor patient dashboard test setup logic

# Improve readability of patient dashboard test

import unittest
from app import app, db
from flask_login import login_user
from app.models.models import User, Role, UserRole, Clinic

class TestClinicDashboard(unittest.TestCase):
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

        self.user = self.create_test_user_with_clinic_role()

    def tearDown(self):
        self.transaction.rollback()
        self.connection.close()
        self.app_context.pop()

    def create_test_user_with_clinic_role(self):
        role = Role.query.filter_by(role_name='clinic').first()
        if not role:
            role = Role(role_name='clinic')
            self.session.add(role)
            self.session.commit()

        user = User(
            name='Test Clinic User', 
            email='testclinic@example.com', 
            password='password',
            activated=True
        )
        self.session.add(user)
        self.session.commit()

        user_role = UserRole(user_id=user.id, role_id=role.id)
        self.session.add(user_role)
        self.session.commit()

        clinic = Clinic(user_id=user.id, phone='0123456789', address='Test Address')
        self.session.add(clinic)
        self.session.commit()

        return user

    def test_clinic_dashboard_get(self):
        with self.app as client:
            with client.session_transaction() as session:
                session['_user_id'] = str(self.user.id)
    
            result = client.get('/clinic_dashboard', follow_redirects=True)
            
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'clinic', result.data)

if __name__ == '__main__':
    unittest.main()

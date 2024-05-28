import os
from app.models.models import *


def create_admin_user():
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    admin_password = os.getenv('ADMIN_PASSWORD', 'pa$$word')

    existing_admin = User.query.join(Role).filter(User.email == admin_email, Role.role_name == 'admin').first()

    if not existing_admin:
        admin_user = User(
            name='Admin',
            email=admin_email,
            password_hash=admin_password
        )
        admin_role = Role(
            role_name='Admin',
            user=admin_user
        )

        db.session.add(admin_user)
        db.session.add(admin_role)
        db.session.commit()


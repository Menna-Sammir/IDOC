import os
from app.models.models import *


def create_admin_user():
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    admin_password = os.getenv('ADMIN_PASSWORD', 'pa$$word')
    admin_role = Role.query.filter_by(role_name='admin').first_or_404()

    existing_admin = User.query.join(UserRole).filter(User.email == admin_email, UserRole.role_id == admin_role.id).first()

    if not existing_admin:
        logo_path ='static/img/user.svg'
        admin_user = User(
            name='Admin',
            email=admin_email,
            password_hash=admin_password,
            photo=logo_path
        )
        admin_role = UserRole(
            role_id= admin_role.id,
            user=admin_user
        )

        db.session.add(admin_user)
        db.session.add(admin_role)
        db.session.commit()


from app.models.models import *

def seed_roles():
    roles = [
        'Admin',
        'doctor',
        'clinic',
        'patient'
    ]

    for name in roles:
        if not Role.query.filter_by(role_name=name).first():
            new_role = Role(role_name=name)
            db.session.add(new_role)
        db.session.commit()

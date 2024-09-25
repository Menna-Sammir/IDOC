from app import app, db, socketio
from app.models.adminUser import *
from app.models.addGovs import *
from app.models.addspecalties import *
from app.models.addRoles import *
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required


def initialize_app():
    with app.app_context():
        db.create_all()
        seed_governorates()
        seed_roles()
        create_admin_user()
        create_specialties()


if __name__ == '__main__':
    initialize_app()
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)

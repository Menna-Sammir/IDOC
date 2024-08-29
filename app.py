from app import app, db, socketio
from app.models.adminUser import *
from app.models.addGovs import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_governorates()
        create_admin_user()
    socketio.run(app, debug=True)
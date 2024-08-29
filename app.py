from app import app, db, socketio
from flask_session import Session
from app.models.adminUser import *
from app.models.addGovs import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_governorates()
        create_admin_user()
        
    socketio.run(app, host='0.0.0.0', debug=True)
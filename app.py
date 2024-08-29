from app import app, db, socketio
from flask_session import Session
from app.models.adminUser import *
from app.models.addGovs import *
from app.models.addspecalties import *


def initialize_app():
    with app.app_context():
        db.create_all()
        seed_governorates()
        create_admin_user()
        create_specialties()



if __name__ == '__main__':
    initialize_app()
    port = int(os.environ.get("PORT", 5000))  # Use the PORT environment variable if available
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
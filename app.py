from app import app, db
from app.models.adminUser import *
from app.models.addGovs import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_governorates()
        create_admin_user()
    app.run(debug=True)
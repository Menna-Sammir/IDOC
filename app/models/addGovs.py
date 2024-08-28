from app.models.models import *

def seed_governorates():
    governorate = [
        'Cairo',
        'Giza',
        'Alexandria',
        'Aswan',
        'Asyut',
        'Beheira',
        'Beni Suef',
        'Dakahlia',
        'Damietta',
        'Faiyum',
        'Gharbia',
        'Ismailia',
        'Kafr El Sheikh',
        'Luxor',
        'Matruh',
        'Minya',
        'Monufia',
        'New Valley',
        'North Sinai',
        'Port Said',
        'Qalyubia',
        'Qena',
        'Red Sea',
        'Sharqia',
        'Sohag',
        'South Sinai',
        'Suez'
    ]

    for name in governorate:
        if not Governorate.query.filter_by(governorate_name=name).first():
            new_governorate = Governorate(governorate_name=name)
            db.session.add(new_governorate)
        db.session.commit()

from app.models.models import *


def create_specialties():
    specialties = [
        ('Anesthesiology', 'static/img/specialities/anesthesiology.png'),
        ('Cardiology', 'static/img/specialities/cardiology.png'),
        ('Dermatology', 'static/img/specialities/dermatology.png'),
        ('Endocrinology', 'static/img/specialities/endocrinology.png'),
        ('Family Medicine', 'static/img/specialities/family_medicine.png'),
        ('Gastroenterology', 'static/img/specialities/gastroenterology.png'),
        ('Geriatrics', 'static/img/specialities/geriatrics.png'),
        ('Hematology', 'static/img/specialities/hematology.png'),
        ('Immunology', 'static/img/specialities/immunology.png'),
        ('Nephrology', 'static/img/specialities/nephrology.png'),
        ('Neurology', 'static/img/specialities/neurology.png'),
        ('Obstetrics', 'static/img/specialities/obstetrics.png'),
        ('Oncology', 'static/img/specialities/oncology.png'),
        ('Ophthalmology', 'static/img/specialities/ophthalmology.png'),
        ('Orthopedics', 'static/img/specialities/orthopedics.png'),
        ('Otolaryngology', 'static/img/specialities/otolaryngology.png'),
        ('Pediatrics', 'static/img/specialities/pediatrics.png'),
        ('Physical Medicine',
            'static/img/specialities/physical-therapy.png'),
        ('Plastic Surgery', 'static/img/specialities/plastic-surgery.png'),
        ('Psychiatry', 'static/img/specialities/psychiatry.png'),
        ('Pulmonology', 'static/img/specialities/pulmonology.png'),
        ('Radiology', 'static/img/specialities/radiology.png'),
        ('Rheumatology', 'static/img/specialities/rheumatology.png'),
        ('Surgery', 'static/img/specialities/surgery.png'),
        ('Emergency Medicin', 'static/img/specialities/emergency-medicine.png'),
        ('Urology', 'static/img/specialities/urology.png')
    ]

    for name, img in specialties:
        if not Specialization.query.filter_by(specialization_name=name).first():
            new_specialty = Specialization(specialization_name=name, photo=img)
            db.session.add(new_specialty)
    db.session.commit()

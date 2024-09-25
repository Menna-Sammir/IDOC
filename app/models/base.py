from app import db
import uuid
from sqlalchemy.dialects.mysql import VARCHAR
from app.models.models import *

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(VARCHAR(60), primary_key=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'id' not in kwargs or not kwargs.get('id'):
            self.id = str(uuid.uuid4())

    # for debugging
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    def all(self, cls=None):
        classes = {"User": User, "Doctor": Doctor, "Patient": Patient,
                   "Appointment": Appointment, "Clinic": Clinic,
                   "Message": Message, "Specialization": Specialization,
<<<<<<< HEAD
                   "Governorate": Governorate, "Role": Role}
=======
                   "Governorate": Governorate, "Role": Role, "UserRole": UserRole, "PatientHistory":PatientHistory, PatientMedicine: "PatientMedicine", MedicineTimes:"MedicineTimes"}
>>>>>>> 43f670543734e42f1cbe595ce9a8b1d215f97291
        records = {}
        if cls is None:
            for class_name, model_class in classes.items():
                records[class_name] = model_class.query.all()
        else:
            records[cls.__name__] = cls.query.all()
        return records

    def add(self, cls, data):
        new_instance = cls(**data)
        db.session.add(new_instance)
        db.session.commit()
        return new_instance

    def count(self, cls=None):
        classes = {"User": User, "Doctor": Doctor, "Patient": Patient,
                   "Appointment": Appointment, "Clinic": Clinic,
                   "Message": Message, "Specialization": Specialization,
<<<<<<< HEAD
                   "Governorate": Governorate, "Role": Role}
=======
                   "Governorate": Governorate, "Role": Role, "UserRole": UserRole, "PatientHistory": PatientHistory, PatientMedicine: "PatientMedicine", MedicineTimes:"MedicineTimes"}
>>>>>>> 43f670543734e42f1cbe595ce9a8b1d215f97291
        if cls:
            return db.session.query(cls).count()
        return sum(db.session.query(cls).count() for cls in classes.values())

    def get(self, cls, id):
        return db.session.query(cls).get(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

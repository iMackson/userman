from pytz import timezone
from db import db
import enum
from sqlalchemy import func, desc

class GenderEnum(str, enum.Enum):
    M = 'M'
    F = 'F'

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80)) 
    gender = db.Column(
        db.Enum(GenderEnum),
        default = GenderEnum.M,
        nullable = False
    )
    date_of_birth = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now(), default=func.now())


    def __init__(self, firstname, lastname, gender, date_of_birth):
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.date_of_birth = date_of_birth
    
    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.last_name)

    def json(self):
        return {
            'id': self.id,
       	    'firstname': self.firstname,
	        'lastname': self.lastname,
	        'gender': self.gender,
	        'date_of_birth': self.date_of_birth.strftime('%m-%d-%Y'),
	        'date_created': self.date_created.strftime('%m-%d-%YT%T'),
            'date_updated': self.date_updated.strftime('%m-%d-%YT%T')
        }

    @classmethod
    def filter_by_parameters(cls, filter_field, filter_value, sort_field):
        if filter_field == 'firstname':
            return {'users': [user.json() for user in cls.query.filter_by(firstname=filter_value).order_by(sort_field).all()]}
        elif filter_field == 'lastname':
            return {'users': [user.json() for user in cls.query.filter_by(lastname=filter_value).order_by(sort_field).all()]}
        elif filter_field == 'gender':
            return {'users': [user.json() for user in cls.query.filter_by(gender=filter_value).order_by(sort_field).all()]}
        else:
            return {'message': 'Filter is not recognised.'}


    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    

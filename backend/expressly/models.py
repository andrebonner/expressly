import email
from enum import unique
import random
from uuid import uuid4
from expressly import db, bcrypt
from datetime import datetime
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    @classmethod
    def seed(self, fake):
        user = User(name=fake.name(), email=fake.email(), password=bcrypt.generate_password_hash(
            "password").decode('utf-8'), is_admin=False)
        db.session.add(user)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}', '{self.is_admin}')"


inst_areas = db.Table('inst_areas',
                      db.Column("institution_id", db.Integer, db.ForeignKey(
                          "institutions.id")),
                      db.Column("area_id", db.Integer, db.ForeignKey(
                          "areas.id"))
                      )


class Area(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    institutions = db.relationship(
        'Institution', secondary=inst_areas, backref='areas', lazy=True)
    schedules = db.relationship('Schedule', backref='area', lazy=True)

    @classmethod
    def seed(self, fake):
        area_code = ''
        while True:
            area_code = fake.city_suffix()
            a = Area.query.filter_by(code=area_code).first()
            if a is None:
                break
        area = Area(code=area_code, name=fake.city())
        db.session.add(area)

    def __repr__(self):
        return f"Area('{self.code}', '{self.name}', '{self.institutions}')"


class Institution(db.Model):
    __tablename__ = 'institutions'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    schedules = db.relationship('Schedule', backref='institution', lazy=True)

    @classmethod
    def seed(self, fake):
        inst_type = ['church', 'space']
        inst_code = ''
        while True:
            inst_code = fake.city_suffix()
            a = Institution.query.filter_by(code=inst_code).first()
            if a is None:
                break
        institution = Institution(code=inst_code, name=fake.company(), email=fake.email(),
                                  telephone=fake.phone_number(), address=fake.address(),  type=inst_type[random.randint(0, len(inst_type)-1)])
        db.session.add(institution)

    def __repr__(self):
        return f"Institution('{self.code}', '{self.name}','{self.email}', '{self.telephone}', '{self.address}',  '{self.type}', '{self.areas}')"


class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    institution_code = db.Column(db.String(50), db.ForeignKey(
        'institutions.code'), nullable=False)
    area_code = db.Column(db.String(50), db.ForeignKey(
        'areas.code'), nullable=False)
    space_count = db.Column(db.Integer, nullable=False)

    @classmethod
    def seed(self, fake):
        area = Area.query.all()
        institution = Institution.query.all()
        for i in range(len(area)):
            for j in range(len(institution)):
                schedule = Schedule(date=datetime.now().date(), time=datetime.now().time(),
                                    institution_code=institution[j].code, area_code=area[i].code, space_count=random.randint(10, 100))
                db.session.add(schedule)

    def __repr__(self):
        return f"Schedule('{self.date}', '{self.time}', '{self.institution_code}', '{self.area_code}', '{self.space_count}')"


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey(
        'schedules.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    space_count = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    @classmethod
    def seed(self, fake):
        schedule = Schedule.query.all()
        user = User.query.all()
        for i in range(len(schedule)):
            for j in range(len(user)):
                booking = Booking(schedule_id=schedule[i].id, user_id=user[j].id,
                                  space_count=random.randint(1, 5), status=random.randint(1, 3))
                db.session.add(booking)

    def __repr__(self):
        return f"Booking('{self.schedule_id}', '{self.user_id}', '{self.space_count}')"

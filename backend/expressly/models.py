import email
from enum import unique
import random
from uuid import uuid4
from expressly import db, bcrypt
from datetime import datetime, timedelta
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
    telephone = db.Column(db.String(20), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False)
    bookings = db.relationship(
        'Booking', backref='user', lazy=True, cascade='all')
    account_type_id = db.Column(db.Integer, db.ForeignKey(
        'account_types.id'), nullable=False)
    institution = db.relationship(
        'Institution', backref='user', lazy=True, cascade='all')
    photo = db.relationship('UserPhoto', backref='user',
                            lazy=True, cascade='all', uselist=False)

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
            "password").decode('utf-8'), telephone=fake.phone_number(), account_type_id=random.randint(1, 3), is_admin=False)
        db.session.add(user)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}', '{self.is_admin}')"


inst_areas = db.Table('inst_areas',
                      db.Column("institution_id", db.Integer, db.ForeignKey(
                          "institutions.id", ondelete="SET NULL")),
                      db.Column("area_id", db.Integer, db.ForeignKey(
                          "areas.id", ondelete="SET NULL"))
                      )


class Area(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    institutions = db.relationship(
        'Institution', secondary=inst_areas, backref='areas', lazy=True, cascade='all')
    schedules = db.relationship(
        'Schedule', backref='area', lazy=True, cascade='all')

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
    schedules = db.relationship(
        'Schedule', backref='institution', lazy=True, cascade='all')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

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
                                  telephone=fake.phone_number(), address=fake.address(),  type=inst_type[random.randint(0, len(inst_type)-1)], user_id=random.randint(1, 5))
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
    booking = db.relationship(
        'Booking', backref='schedule', lazy=True, cascade='all')

    @classmethod
    def seed(self, fake):
        area = Area.query.all()
        institution = Institution.query.all()
        for i in range(len(area)):
            for j in range(len(institution)):
                schedule = Schedule(date=(datetime.now()+timedelta(days=random.randint(1, 4))).date(), time=datetime.now().time(),
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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

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


class AccountType(db.Model):
    __tablename__ = 'account_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user = db.relationship('User',backref='account_type',lazy=True, cascade='all', uselist=False)

    @classmethod
    def seed(self, fake):
        account_type = ['user', 'church', 'space', 'wholesale']
        for i in range(len(account_type)):
            a = AccountType.query.filter_by(name=account_type[i]).first()
            if a is None:
                account = AccountType(name=account_type[i])
                db.session.add(account)

    def __repr__(self):
        return f"AccountType('{self.name}')"


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    items = db.relationship(
        'Item', backref='category', lazy=True, cascade='all', uselist=False)

    @classmethod
    def seed(self, fake):
        categories = ['Food', 'Drink', 'Snack', 'Other']
        for i in range(len(categories)):
            c = Category.query.filter_by(name=categories[i]).first()
            if c is None:
                category = Category(name=categories[i])
                db.session.add(category)

    def __repr__(self):
        return f"Category('{self.name}')"


class UserPhoto(db.Model):
    __tablename__ = 'user_photos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    # user = db.relationship('User', backref='user_photo', lazy=True, cascade='all', uselist=False)

    @classmethod
    def seed(self, fake):
        user = User.query.all()
        for i in range(len(user)):
            p = UserPhoto.query.filter_by(user_id=user[i].id).first()
            if p is None:
                photo = UserPhoto(
                    user_id=user[i].id, url=fake.image_url(width=400, height=400))
                db.session.add(photo)

    def __repr__(self):
        return f"UserPhoto('{self.user_id}', '{self.photo}')"


class Wholesale(db.Model):
    __tablename__ = 'wholesales'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey(
        'institutions.id'), nullable=False)
    items = db.relationship('Item', backref='wholesale',
                            lazy=True, cascade='all')

    @classmethod
    def seed(self, fake):
        wholesale = Wholesale(name=fake.company(),
                              institution_id=random.randint(1, len(Institution.query.all())))
        db.session.add(wholesale)

    def __repr__(self):
        return f"Wholesale('{self.name}', '{self.institution_id}')"


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=False)
    wholesale_id = db.Column(db.Integer, db.ForeignKey(
        'wholesales.id'), nullable=False)
    photo = db.relationship('ItemPhoto', backref='item',
                            lazy=True, cascade='all', uselist=False)
    carts = db.relationship('CartItem', back_populates='item')

    @classmethod
    def seed(self, fake):
        category = Category.query.all()
        wholesale = Wholesale.query.all()
        for i in range(len(category)):
            for j in range(len(wholesale)):
                item = Item(name=fake.word(), description=fake.text(),
                            content=fake.text(), price=random.randint(100, 1000), quantity=random.randint(1, 10), category_id=category[i].id, wholesale_id=wholesale[j].id)
                db.session.add(item)

    def __repr__(self):
        return f"Item('{self.name}', '{self.description}', '{self.content}', '{self.price}', '{self.quantity}', '{self.category_id}', '{self.wholesale_id}')"

    @classmethod
    def seed(self, fake):
        wholesale = Wholesale.query.all()
        for i in range(len(wholesale)):
            item = Item(name=fake.word(), description=fake.text(),
                        content=fake.text(), price=random.randint(100, 1000), quantity=random.randint(1, 10), category_id=random.randint(1, 5), wholesale_id=wholesale[i].id)
            db.session.add(item)

    def __repr__(self):
        return f"Item('{self.name}', '{self.description}', '{self.content}', '{self.price}', '{self.quantity}', '{self.wholesale_id}')"


class ItemPhoto(db.Model):
    __tablename__ = 'item_photos'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey(
        'items.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)

    @classmethod
    def seed(self, fake):
        item = Item.query.all()
        for i in range(len(item)):
            p = ItemPhoto.query.filter_by(item_id=item[i].id).first()
            if p is None:
                photo = ItemPhoto(
                    item_id=item[i].id, url=fake.image_url(width=400, height=400))
                db.session.add(photo)

    def __repr__(self):
        return f"ItemPhoto('{self.item_id}', '{self.url}')"

    @classmethod
    def seed(self, fake):
        item = Item.query.all()
        for i in range(len(item)):
            p = ItemPhoto.query.filter_by(item_id=item[i].id).first()
            if p is None:
                photo = ItemPhoto(
                    item_id=item[i].id, url=fake.image_url(width=400, height=400))
                db.session.add(photo)

    def __repr__(self):
        return f"ItemPhoto('{self.item_id}', '{self.photo}')"


class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    items = db.relationship('CartItem', back_populates='cart')
    status = db.Column(db.String(100), nullable=False, default='pending')
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @classmethod
    def seed(self, fake):
        user = User.query.all()
        for i in range(len(user)):
            cart = Cart(user_id=user[i].id, total=random.randint(100, 1000))
            db.session.add(cart)

    def __repr__(self):
        return f"Cart('{self.user_id}', '{self.total}')"


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey(
        'carts.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey(
        'items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    item = db.relationship('Item', back_populates='carts')
    cart = db.relationship('Cart', back_populates='items')

    @classmethod
    def seed(self, fake):
        cart = Cart.query.all()
        item = Item.query.all()
        for i in range(len(cart)):
            for j in range(len(item)):
                cart_item = CartItem(cart_id=cart[i].id, item_id=item[j].id,
                                     quantity=random.randint(1, 10), total=random.randint(100, 1000))
                db.session.add(cart_item)

    def __repr__(self):
        return f"CartItem('{self.cart_id}', '{self.item_id}', '{self.quantity}', '{self.total}')"

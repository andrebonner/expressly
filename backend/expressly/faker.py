import random
from faker import Faker
from expressly.models import User, Area, Institution, Schedule, Booking, AccountType, Category, UserPhoto, Wholesale, Item, ItemPhoto, InstPhoto
from expressly import db

fake = Faker()


def area_seed():
    for _ in range(5):
        Area.seed(fake)
    db.session.commit()


def institution_seed():
    for _ in range(5):
        Institution.seed(fake)
    db.session.commit()


def institution_area_seed():
    institutions = Institution.query.all()
    for institution in institutions:
        area = Area.query.filter_by(
            id=random.randint(1, 3)).first()
        institution.areas.append(area)
    db.session.commit()


def schedule_seed():
    Schedule.seed(fake)
    db.session.commit()


def booking_seed():
    Booking.seed(fake)
    db.session.commit()


def user_seed():
    for _ in range(3):
        User.seed(fake)
    db.session.commit()


def account_type_seed():
    AccountType.seed(fake)
    db.session.commit()


def category_seed():
    Category.seed(fake)
    db.session.commit()


def user_photo_seed():
    UserPhoto.seed(fake)
    db.session.commit()


def wholesale_seed():
    Wholesale.seed(fake)
    db.session.commit()


def item_seed():
    Item.seed(fake)
    db.session.commit()


def item_photo_seed():
    ItemPhoto.seed(fake)
    db.session.commit()


def inst_photo_seed():
    InstPhoto.seed(fake)
    db.session.commit()

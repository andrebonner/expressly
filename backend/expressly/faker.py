import random
from faker import Faker
from expressly.models import User, Area, Institution, Schedule, Booking
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
    # areas = Area.query.all()
    # for area in areas:
    #     institution = Institution.query.filter_by(
    #         id=random.randint(1, 3)).first()
    #     area.institutions.append(institution)
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

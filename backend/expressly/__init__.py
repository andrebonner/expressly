from flask import Flask
from flask_cors import CORS
from .extensions import db, bcrypt, mail
from expressly.config import Config
from expressly.models import *


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from expressly.auth.routes import auth
    from expressly.areas.routes import areas
    from expressly.bookings.routes import bookings
    from expressly.institutions.routes import institutions
    from expressly.schedules.routes import schedules
    from expressly.main.routes import main
    from expressly.errors.handlers import errors

    app.register_blueprint(auth, url_prefix='/api')
    app.register_blueprint(areas, url_prefix='/api')
    app.register_blueprint(bookings, url_prefix='/api')
    app.register_blueprint(institutions, url_prefix='/api')
    app.register_blueprint(schedules, url_prefix='/api')
    app.register_blueprint(main)
    app.register_blueprint(errors)

    with app.app_context():
        db.create_all()
        db.session.commit()
        # from expressly.faker import user_seed, area_seed, institution_seed, institution_area_seed, schedule_seed, booking_seed
        # user_seed()
        # area_seed()
        # institution_seed()
        # institution_area_seed()
        # schedule_seed()
        # booking_seed()

    return app

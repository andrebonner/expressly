from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from expressly.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from expressly.main.routes import main
    from expressly.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)

    # with app.app_context():
    #     db.create_all()
    #     db.session.commit()
    #     from expressly.faker import user_seed, post_seed
    #     user_seed()
    #     post_seed()

    return app

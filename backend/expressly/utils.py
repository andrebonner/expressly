from functools import wraps
import random
from sre_constants import MAGIC
import string
from flask_mail import Message
from expressly.extensions import mail
from flask import request, jsonify, current_app
from expressly.models import User
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return jsonify({'error': 'Token is missing'}), 401

        token = request.headers.get('Authorization').split()[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        data = []
        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


def generate_random_password():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


def send_email(email, subject, body, html=False, attachments=None):
    email.append('andrebonner@hotmail.com')
    try:
        msg = Message(
            subject, sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=email)
        if html == True:
            msg.html = body
        else:
            msg.body = body
        # TODO: test sending attachments
        if attachments is not None:
            for attachment in attachments:
                mime = MAGIC.from_file(attachment, mime=True)
                with open(attachment, 'rb') as f:
                    msg.attach(attachment, mime, f.read())

        mail.send(msg)
    except Exception as e:
        print(e)
        return False

    return True

import datetime
from flask import Blueprint, jsonify, request, current_app
from expressly.utils import token_required
import jwt
from expressly.extensions import bcrypt, db
from expressly.models import User


auth = Blueprint('auth', __name__)


@auth.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user is not None:
        return jsonify({'success': False, 'message': 'User already exists'})
    user = User(name=data['name'], email=data['email'], password=bcrypt.generate_password_hash(
        data['password']).decode('utf-8'), is_admin=False)
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'User created'})


@auth.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['username']).first()
    if user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 401
    if bcrypt.check_password_hash(user.password, data['password']):
        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
        return jsonify({'success': True, 'message': 'User logged in', 'token': token})
    return jsonify({'success': False, 'message': 'Invalid password'}), 401


@auth.route('/auth/user', methods=['GET'])
@token_required
def get_user(current_user):
    if current_user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 401

    user = {'id': current_user.id, 'email': current_user.email,
            'name': current_user.name, 'is_admin': current_user.is_admin, 'bookings': []}
    for booking in current_user.bookings:
        user['bookings'].append({'id': booking.id, 'date': booking.schedule.date, 'time': str(booking.schedule.time),
                                 'area': booking.schedule.area.name, 'institution': booking.schedule.institution.name})

    return jsonify({'success': True,  'user': user})


@auth.route('/auth/logout', methods=['POST'])
def logout():
    return jsonify({'success': True})

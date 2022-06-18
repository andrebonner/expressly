import datetime
from flask import Blueprint, jsonify, request, current_app
from expressly.utils import token_required
import jwt
from expressly.extensions import bcrypt, db
from expressly.models import User


users = Blueprint('users', __name__)


@users.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    if current_user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 401

    users = User.query.all()
    us = []
    for user in users:
        u = {'id': user.id, 'email': user.email,
             'name': user.name, 'is_admin': user.is_admin, 'bookings': []}
        for booking in user.bookings:
            u['bookings'].append({'id': booking.id, 'date': booking.schedule.date, 'time': str(booking.schedule.time),
                                  'area': {'id': booking.schedule.area.id, 'code': booking.schedule.area.code, 'name': booking.schedule.area.name},
                                  'institution': {'id': booking.schedule.institution.id, 'code': booking.schedule.institution.code, 'name': booking.schedule.institution.name, 'type': booking.schedule.institution.type, 'address': booking.schedule.institution.address, 'telephone': booking.schedule.institution.telephone, 'email': booking.schedule.institution.email}})
        us.append(u)
    return jsonify(us)


@users.route('/users/<int:id>', methods=['GET'])
@token_required
def get_user(current_user, id):
    if current_user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 401

    user = User.query.filter_by(id=id).first()
    if user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 401

    u = {'id': user.id, 'email': user.email, 'name': user.name,
         'is_admin': user.is_admin, 'bookings': []}
    for booking in user.bookings:
        u['bookings'].append({'id': booking.id, 'date': booking.schedule.date, 'time': str(booking.schedule.time),
                              'area': {'id': booking.schedule.area.id, 'code': booking.schedule.area.code, 'name': booking.schedule.area.name},
                              'institution': {'id': booking.schedule.institution.id, 'code': booking.schedule.institution.code, 'name': booking.schedule.institution.name, 'type': booking.schedule.institution.type, 'address': booking.schedule.institution.address, 'telephone': booking.schedule.institution.telephone, 'email': booking.schedule.institution.email}})
    return jsonify(u)


@users.route('/users', methods=['POST'])
@token_required
def create_user(current_user):
    if current_user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 401
    data = request.get_json()
    if data is None:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    if 'email' not in data or 'name' not in data or 'password' not in data:
        return jsonify({'success': False, 'message': 'Missing data'}), 400
    if User.query.filter_by(email=data['email']).first() is not None:
        return jsonify({'success': False, 'message': 'User already exists'}), 400
    user = User(email=data['email'], name=data['name'], password=bcrypt.generate_password_hash(
        data['password']).decode('utf-8'), is_admin=False)
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'User created'})


@users.route('/users/<int:id>', methods=['PUT'])
@token_required
def update_user(current_user, id):
    if current_user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 401
    data = request.get_json()
    if data is None:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    if 'email' not in data or 'name' not in data:
        return jsonify({'success': False, 'message': 'Missing data'}), 400
    user = User.query.filter_by(id=id).first()
    if user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 401
    user.email = data['email']
    user.name = data['name']
    db.session.commit()
    return jsonify({'success': True, 'message': 'User updated'})


@users.route('/users/<int:id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    if current_user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 401
    user = User.query.filter_by(id=id).first()
    if user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 401
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'User deleted'})

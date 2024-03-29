import datetime
from flask import Blueprint, jsonify, request, current_app
from expressly.utils import send_email, token_required
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
        data['password']).decode('utf-8'), telephone='', is_admin=False)
    db.session.add(user)
    db.session.commit()
    # Send email notification for newly created user
    if send_email([user.email], 'Welcome to Expressly', f'''Welcome {user.name},  \nThis website allows you to book space or church services. \n\nTo login, please visit https://expressly.io/login \n\nThank you for using Expressly!'''):
        return jsonify({'success': True, 'message': 'User created'})
    else:
        return jsonify({'success': True, 'message': 'User created, Error sending email'})


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
            'name': current_user.name, 'telephone': current_user.telephone, 'is_admin': current_user.is_admin, 'account_type': {'id': current_user.account_type.id, 'name': current_user.account_type.name}}
    if current_user.photo is not None:
        user['photo'] = {'url': current_user.photo.url,
                         'id': current_user.photo.id}

    # church or space
    if current_user.account_type.name == 'church' or current_user.account_type.name == 'space' and current_user.institution.id is not None:
        user['institution'] = {'id': current_user.institution.id, 'name': current_user.institution.name, 'code': current_user.institution.code, 'type': current_user.institution.type, 'telephone': current_user.institution.telephone,
                               'email': current_user.institution.email, 'address': current_user.institution.address, 'photo': {'url': current_user.institution.photo.url, 'id': current_user.institution.photo.id}, 'schedules': []}
        for schedule in current_user.institution.schedules:
            user['institution']['schedules'].append(
                {'id': schedule.id, 'date': schedule.date, 'time': str(schedule.time), 'space_count': schedule.space_count, 'area': {'id': schedule.area.id,
                                                                                                                                     'code': schedule.area.code, 'name': schedule.area.name}, 'booking': {}})

    # wholesale
    elif current_user.account_type.name == 'wholesale' and current_user.institution.id is not None:
        user['institution'] = {'id': current_user.institution.id, 'name': current_user.institution.name, 'code': current_user.institution.code, 'type': current_user.institution.type, 'telephone': current_user.institution.telephone,
                               'email': current_user.institution.email, 'address': current_user.institution.address, 'photo': {'url': current_user.institution.photo.url, 'id': current_user.institution.photo.id}}
        if current_user.institution.wholesale is not None:
            user['institution']['wholesale'] = {
                'id': current_user.institution.wholesale.id, 'name': current_user.institution.wholesale.name, 'items': []}
            for item in current_user.institution.wholesale.items:
                user['institution']['wholesale']['items'].append(
                    {'id': item.id, 'name': item.name, 'price': item.price, 'quantity': item.quantity, 'description': item.description, 'content': item.content, 'category': {'id': item.category.id, 'name': item.category.name}, 'photo': {'url': item.photo.url, 'id': item.photo.id}})
    else:
        user['bookings'] = []
        user['cart'] = {}
        for booking in current_user.bookings:
            user['bookings'].append({'id': booking.id, 'schedule': {'date': booking.schedule.date, 'time': str(booking.schedule.time),
                                                                    'area': {'id': booking.schedule.area.id, 'code': booking.schedule.area.code, 'name': booking.schedule.area.name},
                                                                    'institution': {'id': booking.schedule.institution.id, 'code': booking.schedule.institution.code, 'name': booking.schedule.institution.name, 'type': booking.schedule.institution.type, 'address': booking.schedule.institution.address, 'telephone': booking.schedule.institution.telephone, 'email': booking.schedule.institution.email}}})
        if current_user.cart is not None:
            user['cart'] = {'id': current_user.cart.id, 'items': []}
            for item in current_user.cart.items:
                user['cart']['items'].append(
                    {'id': item.id, 'name': item.item.name, 'price': item.item.price, 'quantity': item.quantity, 'total': item.total})

    return jsonify({'success': True,  'user': user})


@ auth.route('/auth/logout', methods=['POST'])
def logout():
    return jsonify({'success': True})


@ auth.route('/auth/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user is None:
        return jsonify({'success': False, 'message': 'User does not exist'}), 401
    token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
    # Send email with link to verify user requested a change
    if send_email([user.email], 'Expressly - Password Reset',
                  f'''Hello {user.name}, \n\nYou have requested a password reset. \n\nTo reset your password, please visit https://expressly.io/reset-password?token={token} \n\nThank you for using Expressly!'''):
        return jsonify({'success': True, 'message': 'Password reset email sent'})
    else:
        return jsonify({'success': False, 'message': 'Password reset email could not be sent!'})


@auth.route('/auth/reset_password', methods=['GET'])
@token_required
def get_reset_user(current_user):
    if current_user is None:
        return jsonify({'success': False, 'message': 'User does not exist!'}), 401
    return jsonify({'success': True, 'user': {'id': current_user.id, 'email': current_user.email,
                                              'name': current_user.name, 'telephone': current_user.telephone, 'is_admin': current_user.is_admin, 'bookings': []}})


@auth.route('/auth/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user is None:
        return jsonify({'success': False, 'message': 'User does not exist!'}), 401
    user.password = bcrypt.generate_password_hash(
        data['password']).decode('utf-8')
    db.session.commit()
    return jsonify({'success': True, 'message': 'User password reset successfully'})

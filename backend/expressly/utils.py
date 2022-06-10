from functools import wraps
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

from flask import Blueprint, jsonify


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return jsonify({'message': 'Hello, World!'})

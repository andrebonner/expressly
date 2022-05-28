from flask import Blueprint, jsonify

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(500)
def error_500(error):
    return jsonify({'message': 'Internal Server Error'}), 500


@errors.app_errorhandler(404)
def error_404(error):
    return jsonify({'message': 'Not Found'}), 404


@errors.app_errorhandler(403)
def error_403(error):
    return jsonify({'message': 'Forbidden'}), 403

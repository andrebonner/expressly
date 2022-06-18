from flask import Blueprint, jsonify, request
from expressly.models import Area, Institution
from expressly.utils import token_required
from expressly.extensions import db


areas = Blueprint('areas', __name__)


@areas.route('/areas', methods=['GET'])
def index():
    areas = Area.query.all()
    aes = []
    for area in areas:
        a = {
            'code': area.code,
            'name': area.name,
            'institutions': []
        }
        for institution in area.institutions:
            a['institutions'].append(
                {'code': institution.code, 'name': institution.name})
        aes.append(a)
    return jsonify(aes)


@areas.route('/areas/<type>', methods=['GET'])
def show(type):
    institutions = Institution.query.filter_by(type=type).all()
    insts = []
    for institution in institutions:
        for area in institution.areas:
            if next((a for a in insts if a['code'] == area.code), None) is None:
                a = {'code': area.code, 'name': area.name}
                insts.append(a)
    return jsonify(insts)


@areas.route('/areas/<type>/<code>', methods=['GET'])
def show_by_code(type, code):
    institution = Institution.query.filter_by(type=type, code=code).first()
    if institution is None:
        return jsonify({'error': 'institution not found'})
    areas = institution.areas
    aes = []
    for area in areas:
        a = {
            'code': area.code,
            'name': area.name,
            'institutions': []
        }
        for institution in area.institutions:
            a['institutions'].append(
                {'code': institution.code, 'name': institution.name})
        aes.append(a)
    return jsonify(aes)


@areas.route('/areas', methods=['POST'])
@token_required
def create(current_user):
    if not current_user.admin:
        return jsonify({'success': False, 'message': 'permission denied'})
    data = request.get_json()
    area = Area(code=data['code'], name=data['name'])
    db.session.add(area)
    db.session.commit()
    return jsonify({'success': True, 'message': 'area created'})


@areas.route('/areas/<code>', methods=['PUT'])
@token_required
def update(current_user, code):
    if not current_user.admin:
        return jsonify({'success': False, 'message': 'permission denied'})
    data = request.get_json()
    area = Area.query.filter_by(code=code).first()
    if area is None:
        return jsonify({'error': 'area not found'})
    area.name = data['name']
    db.session.commit()
    return jsonify({'success': True, 'message': 'area updated'})


@areas.route('/areas/<code>', methods=['DELETE'])
@token_required
def delete(current_user, code):
    if not current_user.admin:
        return jsonify({'success': False, 'message': 'permission denied'})
    area = Area.query.filter_by(code=code).first()
    if area is None:
        return jsonify({'error': 'area not found'})
    db.session.delete(area)
    db.session.commit()
    return jsonify({'success': True, 'message': 'area deleted'})

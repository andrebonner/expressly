from flask import Blueprint, jsonify, request
from expressly.models import Area, Institution
from expressly.utils import token_required
from expressly.extensions import db

institutions = Blueprint('institutions', __name__)


@institutions.route('/institutions', methods=['GET'])
def index():
    institutions = Institution.query.all()
    insts = []
    for institution in institutions:
        i = {
            'id': institution.id,
            'code': institution.code,
            'name': institution.name,
            'type': institution.type,
            'telephone': institution.telephone,
            'email': institution.email,
            'address': institution.address,
            'areas': []
        }
        for area in institution.areas:
            i['areas'].append({'code': area.code, 'name': area.name})
        insts.append(i)
    return jsonify(insts)


@institutions.route('/institutions/<type>', methods=['GET'])
def show(type):
    institutions = Institution.query.filter_by(type=type).all()
    insts = []
    for institution in institutions:
        if next((i for i in insts if i['code'] == institution.code), None) is None:
            i = {'id': institution.id, 'code': institution.code,
                 'name': institution.name, 'type': institution.type,
                 'telephone': institution.telephone,
                 'email': institution.email,
                 'address': institution.address, }
            insts.append(i)
    return jsonify(insts)


@institutions.route('/institutions', methods=['POST'])
@token_required
def create(current_user):
    if not current_user.is_admin:
        return jsonify({'error': 'permission denied'})
    data = request.get_json()
    institution = Institution(code=data['code'], name=data['name'], type=data['type'],
                              telephone=data['telephone'], address=data['address'], email=data['email'])
    db.session.add(institution)
    db.session.commit()
    return jsonify({'success': True, 'message': 'institution created'})


@institutions.route('/institutions/<code>', methods=['GET'])
def show_by_code(type, code):
    institution = Institution.query.filter_by(code=code).first()
    if institution is None:
        return jsonify({'error': 'institution not found'})
    areas = institution.areas
    aes = []
    for area in areas:
        a = {
            'id': area.id,
            'code': area.code,
            'name': area.name,
            'institutions': []
        }
        for institution in area.institutions:
            a['institutions'].append(
                {'code': institution.code, 'name': institution.name})
        aes.append(a)
    return jsonify(aes)


@institutions.route('/institutions/<code>', methods=['PUT'])
@token_required
def update(current_user,  code):
    if not current_user.is_admin:
        return jsonify({'error': 'permission denied'})
    data = request.get_json()
    institution = Institution.query.filter_by(code=code).first()
    if institution is None:
        return jsonify({'error': 'institution not found'})
    institution.name = data['name']
    institution.telephone = data['telephone']
    institution.address = data['address']
    institution.email = data['email']
    db.session.commit()
    return jsonify({'success': True, 'message': 'institution updated'})


@institutions.route('/institutions/<code>', methods=['DELETE'])
@token_required
def delete(current_user,  code):
    if not current_user.is_admin:
        return jsonify({'error': 'permission denied'})
    institution = Institution.query.filter_by(code=code).first()
    if institution is None:
        return jsonify({'error': 'institution not found'})
    db.session.delete(institution)
    db.session.commit()
    return jsonify({'success': True, 'message': 'institution deleted'})

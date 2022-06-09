from flask import Blueprint, jsonify
from expressly.models import Area, Institution


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

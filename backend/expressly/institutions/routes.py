from flask import Blueprint, jsonify
from expressly.models import Area, Institution

institutions = Blueprint('institutions', __name__)


@institutions.route('/institutions', methods=['GET'])
def index():
    institutions = Institution.query.all()
    insts = []
    for institution in institutions:
        i = {
            'code': institution.code,
            'name': institution.name,
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
            i = {'code': institution.code, 'name': institution.name}
            insts.append(i)
    return jsonify(insts)

from flask import Blueprint, jsonify, request
from expressly.models import Area, Institution, Schedule
from expressly.utils import token_required
from expressly.extensions import db


schedules = Blueprint('schedules', __name__)


@schedules.route('/schedules', methods=['GET'])
def index():
    type = request.args.get('type')
    area = request.args.get('area')
    institution = request.args.get('institution')
    date = request.args.get('date')
    sch = []

    if area is not None and institution is not None and date is not None:
        schedules = Schedule.query.filter_by(
            area_code=area, institution_code=institution, date=date)
    elif area is not None and institution is not None:
        schedules = Schedule.query.filter_by(
            area_code=area, institution_code=institution)
    elif area is not None and date is not None:
        schedules = Schedule.query.filter_by(area_code=area, date=date)
    elif institution is not None and date is not None:
        schedules = Schedule.query.filter_by(
            institution_code=institution, date=date)
    elif area is not None:
        schedules = Schedule.query.filter_by(area_code=area)
    elif institution is not None:
        schedules = Schedule.query.filter_by(institution_code=institution)
    elif date is not None:
        schedules = Schedule.query.filter_by(date=date)
    else:
        schedules = Schedule.query.all()

    for schedule in schedules:
        if type is None or schedule.institution.type == type:
            s = {'id': schedule.id,
                 'area': {'id': schedule.area.id, 'code': schedule.area.code, 'name': schedule.area.name},
                 'institution': {'id': schedule.institution.id, 'code': schedule.institution.code, 'name': schedule.institution.name, 'address': schedule.institution.address, 'telephone': schedule.institution.telephone, 'email': schedule.institution.email},
                 'date': schedule.date.strftime("%x"),
                 'time': str(schedule.time),
                 }
            sch.append(s)
    return jsonify(sch)


@schedules.route('/schedules/<string:type>/<int:id>', methods=['GET'])
def get_schedule(type, id):
    s = {}
    schedule = Schedule.query.filter_by(id=id).first()
    if schedule.institution.type == type:
        s = {'id': schedule.id,
             'code': schedule.area.code,
             'area': schedule.area.name,
             'institution': [],
             'date': schedule.date.strftime("%x"),
             'time': str(schedule.time),
             }
        s['institution'] = {
            'id': schedule.institution.id,
            'code': schedule.institution.code,
            'name': schedule.institution.name,
            'address': schedule.institution.address,
            'telephone': schedule.institution.telephone,
            'email': schedule.institution.email,
        }

    return jsonify(s)


@schedules.route('/schedules/<string:type>/<int:id>', methods=['POST'])
@token_required
def create_schedule(current_user, type, id):
    data = request.get_json()
    area = Area.query.filter_by(id=data['area']).first()
    institution = Institution.query.filter_by(id=data['institution']).first()

    if area is None or institution is None:
        return jsonify({'success': False, 'message': 'area or institution not found'})

    date = data['date']
    time = data['time']
    space_count = data['space_count']
    if space_count > 1:
        schedule = Schedule(area_code=area.code, institution_code=institution.code,
                            date=date, time=time, space_count=space_count)
        db.session.add(schedule)
        db.session.commit()
        return jsonify({'success': True, 'message': 'schedule created'})
    else:
        return jsonify({'success': False, 'message': 'space_count must be greater than 1'})


@schedules.route('/schedules/<string:type>/<int:id>', methods=['PUT'])
@token_required
def update_schedule(type, id):
    data = request.get_json()
    schedule = Schedule.query.filter_by(id=id).first()
    if schedule is None:
        return jsonify({'success': False, 'message': 'schedule not found'})

    if 'area' in data:
        area = Area.query.filter_by(id=data['area']).first()
        if area is None:
            return jsonify({'success': False, 'message': 'area not found'})
        schedule.area_code = area.code
    if 'institution' in data:
        institution = Institution.query.filter_by(
            id=data['institution']).first()
        if institution is None:
            return jsonify({'success': False, 'message': 'institution not found'})
        schedule.institution_code = institution.code
    if 'date' in data:
        schedule.date = data['date']
    if 'time' in data:
        schedule.time = data['time']
    if 'space_count' in data and data['space_count'] > 1:
        schedule.space_count = data['space_count']
    db.session.commit()
    return jsonify({'success': True, 'message': 'schedule updated'})


@schedules.route('/schedules/<string:type>/<int:id>', methods=['DELETE'])
@token_required
def delete_schedule(current_user, type, id):
    if not current_user.admin:
        return jsonify({'success': False, 'message': 'Permission denied'})
    schedule = Schedule.query.filter_by(id=id).first()
    if schedule is None:
        return jsonify({'success': False, 'message': 'schedule not found'})
    db.session.delete(schedule)
    db.session.commit()
    return jsonify({'success': True, 'message': 'schedule deleted'})

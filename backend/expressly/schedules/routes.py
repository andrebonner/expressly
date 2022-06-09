from flask import Blueprint, jsonify, request
from expressly.models import Area, Institution, Schedule


schedules = Blueprint('schedules', __name__)


@schedules.route('/schedules', methods=['GET'])
def index():
    type = request.args.get('type')
    area = request.args.get('area')
    institution = request.args.get('institution')
    date = request.args.get('date')
    sch = []

    if type is None:
        return jsonify({'error': 'type is required'})

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
        if schedule.institution.type == type:
            s = {'id': schedule.id,
                 'area': schedule.area.name,
                 'institution': schedule.institution.name,
                 'date': schedule.date,
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
             'area': schedule.area.name,
             'institution': [],
             'date': schedule.date,
             'time': str(schedule.time),
             }
        s['institution'] = {
            'id': schedule.institution.id,
            'name': schedule.institution.name,
            'address': schedule.institution.address,
            'telephone': schedule.institution.telephone,
            'email': schedule.institution.email,
        }

    return jsonify(s)

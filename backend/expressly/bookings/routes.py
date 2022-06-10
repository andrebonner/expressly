from flask import Blueprint, jsonify, request
from expressly.models import Booking, Schedule
from expressly.utils import token_required
from expressly.extensions import db


bookings = Blueprint('bookings', __name__)


@bookings.route('/bookings', methods=['GET'])
@token_required
def index(current_user):
    if current_user.is_admin:
        bookings = Booking.query.all()
    else:
        bookings = Booking.query.filter_by(user_id=current_user.id)
    bs = []
    for booking in bookings:
        b = {'id': booking.id,  'user_id': booking.user_id,
             'area': booking.schedule.area.name, 'institution': booking.schedule.institution.name,
             'date': booking.schedule.date, 'time': str(booking.schedule.time),
             'status': booking.status}
        bs.append(b)
    return jsonify(bs)


@bookings.route('/bookings/<int:id>', methods=['GET'])
@token_required
def get_booking(current_user, id):
    booking = Booking.query.filter_by(id=id).first()
    if booking is None:
        return jsonify({'error': 'Booking not found'})
    if current_user.is_admin or current_user.id == booking.user_id:
        b = {'id': booking.id,  'user_id': booking.user_id,
             'area': booking.schedule.area.name, 'institution': booking.schedule.institution.name,
             'date': booking.schedule.date, 'time': str(booking.schedule.time),
             'status': booking.status}
        return jsonify(b)
    else:
        return jsonify({'success': False, 'message': 'Unauthorized'})


@bookings.route('/bookings', methods=['POST'])
@token_required
def create_booking(current_user):
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'No data'})
    if current_user.is_admin or current_user.id == data['user_id']:
        schedule = Schedule.query.filter_by(id=data['schedule_id']).first()
        booking = Booking(
            user_id=data['user_id'], schedule_id=data['schedule_id'], space_count=1, status=1)
        db.session.add(booking)
        schedule.space_count -= 1
        # db.session.update(schedule)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Booking created'})
    else:
        return jsonify({'success': False, 'message': 'Unauthorized'})

from flask import Blueprint, jsonify, request
from expressly.models import Wholesale
from expressly.utils import token_required
from expressly.extensions import db

wholesales = Blueprint('wholesale', __name__)


@wholesales.route('/wholesales', methods=['GET'])
def index():
    wholesales = Wholesale.query.all()
    ws = []
    for wholesale in wholesales:
        w = {
            'id': wholesale.id,
            'name': wholesale.name,
        }

        ws.append(w)
    return jsonify(ws)


@wholesales.route('/wholesales/<id>', methods=['GET'])
def show(id):
    wholesale = Wholesale.query.filter_by(id=id).first()
    if wholesale is None:
        return jsonify({'success': False, 'message': 'wholesale not found'})
    w = {
        'id': wholesale.id,
        'name': wholesale.name,
    }
    return jsonify(w)


@wholesales.route('/wholesales', methods=['POST'])
@token_required
def create(current_user):
    if current_user.is_admin:
        return jsonify({'success': False, 'message': 'permission denied'})
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'success': False, 'message': 'no name provided'})
    wholesale = Wholesale(name=name)
    db.session.add(wholesale)
    db.session.commit()
    return jsonify({'success': True, 'message': 'wholesale created'})


@wholesales.route('/wholesales/<id>', methods=['PUT'])
@token_required
def update(current_user, id):
    if current_user.is_admin:
        return jsonify({'success': False, 'message': 'permission denied'})
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'success': False, 'message': 'no name provided'})
    wholesale = Wholesale.query.filter_by(id=id).first()
    if wholesale is None:
        return jsonify({'success': False, 'message': 'wholesale not found'})
    wholesale.name = name
    db.session.commit()
    return jsonify({'success': True, 'message': 'wholesale updated'})


@wholesales.route('/wholesales/<id>', methods=['DELETE'])
@token_required
def delete(current_user, id):
    if current_user.is_admin:
        return jsonify({'success': False, 'message': 'permission denied'})
    wholesale = Wholesale.query.filter_by(id=id).first()
    if wholesale is None:
        return jsonify({'success': False, 'message': 'wholesale not found'})
    db.session.delete(wholesale)
    db.session.commit()
    return jsonify({'success': True, 'message': 'wholesale deleted'})


@wholesales.route('/wholesales/<id>/items', methods=['GET'])
def items(id):
    wholesale = Wholesale.query.filter_by(id=id).first()
    if wholesale is None:
        return jsonify({'success': False, 'message': 'wholesale not found'})
    items = wholesale.items
    is_ = []
    for item in items:
        i = {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'content': item.content,
            'price': item.price,
            'quantity': item.quantity,
            'photo': {'id': item.photo.id, 'url': item.photo.url},
            'category': {'id': item.category.id, 'name': item.category.name},
            'wholesale_id': item.wholesale_id,
        }
        is_.append(i)
    return jsonify(is_)

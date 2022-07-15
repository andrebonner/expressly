from flask import Blueprint, jsonify, request
from expressly.utils import token_required
from expressly.models import Item, ItemPhoto, Category
from expressly.extensions import db

items = Blueprint('items', __name__)


@items.route('/items', methods=['GET'])
def index():
    items = Item.query.all()
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

        }
        is_.append(i)
    return jsonify(is_)


@items.route('/items/<int:id>', methods=['GET'])
def show(id):
    item = Item.query.filter_by(id=id).first()
    if item is None:
        return jsonify({'success': False, 'message': 'item not found'})
    i = {
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'content': item.content,
        'price': item.price,
        'quantity': item.quantity,
        'photo': {'id': item.photo.id, 'url': item.photo.url},
        'category': {'id': item.category.id, 'name': item.category.name},

    }
    return jsonify(i)


@items.route('/items', methods=['POST'])
@token_required
def create(current_user):
    if current_user.is_admin:
        return jsonify({'success': False, 'message': 'permission denied'})
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    content = data.get('content')
    price = data.get('price')
    quantity = data.get('quantity')
    category_id = data.get('category_id')
    photo = data.get('photo')

    if not name:
        return jsonify({'success': False, 'message': 'no name provided'})
    if not description:
        return jsonify({'success': False, 'message': 'no description provided'})
    if not content:
        return jsonify({'success': False, 'message': 'no content provided'})
    if not price:
        return jsonify({'success': False, 'message': 'no price provided'})
    if not quantity:
        return jsonify({'success': False, 'message': 'no quantity provided'})
    if not category_id:
        return jsonify({'success': False, 'message': 'no category provided'})
    if not photo:
        return jsonify({'success': False, 'message': 'no photo provided'})
    item = Item(name=name, description=description, content=content,
                price=price, quantity=quantity, category_id=category_id)
    item_photo = ItemPhoto(item_id=item.id, url=photo)
    db.session.add(item)
    db.session.add(item_photo)
    db.session.commit()
    return jsonify({'success': True, 'message': 'item created'})


@items.route('/items/<int:id>', methods=['PUT'])
@token_required
def update(current_user, id):
    if current_user.is_admin:
        return jsonify({'success': False, 'message': 'permission denied'})
    item = Item.query.filter_by(id=id).first()
    if item is None:
        return jsonify({'success': False, 'message': 'item not found'})
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    content = data.get('content')
    price = data.get('price')
    quantity = data.get('quantity')
    category_id = data.get('category_id')
    photo = data.get('photo')

    if not name:
        return jsonify({'success': False, 'message': 'no name provided'})
    if not description:
        return jsonify({'success': False, 'message': 'no description provided'})
    if not content:
        return jsonify({'success': False, 'message': 'no content provided'})
    if not price:
        return jsonify({'success': False, 'message': 'no price provided'})
    if not quantity:
        return jsonify({'success': False, 'message': 'no quantity provided'})
    if not category_id:
        return jsonify({'success': False, 'message': 'no category provided'})
    if not photo:
        return jsonify({'success': False, 'message': 'no photo provided'})
    item.name = name
    item.description = description
    item.content = content
    item.price = price
    item.quantity = quantity
    item.category_id = category_id

    item_photo = ItemPhoto.query.filter_by(item_id=item.id).first()
    if item_photo is not None:
        item_photo.url = photo
    else:
        item_photo = ItemPhoto(item_id=item.id, url=photo)

    db.session.add(item_photo)
    db.session.commit()
    return jsonify({'success': True, 'message': 'item updated'})


@items.route('/items/<int:id>', methods=['DELETE'])
@token_required
def delete(current_user, id):
    if current_user.is_admin:
        return jsonify({'success': False, 'message': 'permission denied'})
    item = Item.query.filter_by(id=id).first()
    if item is None:
        return jsonify({'success': False, 'message': 'item not found'})
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True, 'message': 'item deleted'})


@items.route('/items/categories', methods=['GET'])
def categories():
    categories = Category.query.all()
    cs = []
    for category in categories:
        c = {
            'id': category.id,
            'name': category.name,
        }
        cs.append(c)
    return jsonify(cs)

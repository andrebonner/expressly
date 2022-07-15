from flask import Blueprint, jsonify, request
from expressly.utils import token_required, send_email
from expressly.extensions import db
from expressly.models import Cart, CartItem, Item

carts = Blueprint('carts', __name__)


@carts.route('/carts', methods=['GET'])
@token_required
def index(current_user):
    carts = Cart.query.filter_by(user_id=current_user.id).all()
    cs = []
    for cart in carts:
        c = {
            'id': cart.id,
            'user_id': cart.user_id,
            'total': cart.total,
            'items': []
        }
        for item in cart.items:
            i = {
                'id': item.id,
                'name': item.item.name,
                'price': item.item.price,
                'quantity': item.quantity,
                'total': item.total,
            }
            c['items'].append(i)
        cs.append(c)
    return jsonify(cs)


@carts.route('/cart', methods=['GET'])
@token_required
def show(current_user):
    cart = Cart.query.filter_by(
        user_id=current_user.id, status='pending').first()
    if cart is None:
        return jsonify({'success': False, 'message': 'cart not found'})
    c = {
        'id': cart.id,
        'user_id': cart.user_id,
        'status': cart.status,
        'total': cart.total,
        'items': []
    }
    for item in cart.items:
        i = {
            'id': item.id,
            'name': item.item.name,
            'description': item.item.description,
            'content': item.item.content,
            'price': item.item.price,
            'photo': {'id': item.item.photo.id, 'url': item.item.photo.url},
            'quantity': item.quantity,
            'total': item.total,
        }
        c['items'].append(i)
    return jsonify(c)


@carts.route('/carts/item', methods=['POST'])
@token_required
def create(current_user):
    data = request.get_json()
    if data is None:
        return jsonify({'success': False, 'message': 'no data'})

    item = Item.query.filter_by(id=data.get('item_id')).first()
    if item is None:
        return jsonify({'success': False, 'message': 'item not found'})

    cart = Cart.query.filter_by(
        user_id=current_user.id, status='pending').first()
    if cart is None:
        cart = Cart(user_id=current_user.id, total=0)
        cart_item = CartItem(item_id=item.id, quantity=data.get(
            'quantity'), total=item.price*data.get('quantity'))
        cart.items.append(cart_item)
        db.session.add(cart)
    else:
        # TODO : check if item in cart
        # c_item = cart.items.filter_by(item_id=item.id).first()
        cart.items.append(item)
        cart.total += item.price
    db.session.commit()
    c = {
        'id': cart.id,
        'user_id': cart.user_id,
        'status': cart.status,
        'items': []
    }
    for item in cart.items:
        i = {
            'id': item.id,
            'name': item.item.name,
            'description': item.item.description,
            'content': item.item.content,
            'price': item.item.price,
            'quantity': item.quantity,
            'photo': {'id': item.item.photo.id, 'url': item.item.photo.url},
            'category': {'id': item.item.category.id, 'name': item.item.category.name},
        }
        c['items'].append(i)
    return jsonify({'success': True, 'message': 'item added to cart', 'cart': c})


@carts.route('/cart/checkout', methods=['PUT'])
@token_required
def checkout(current_user):
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart is None:
        return jsonify({'success': False, 'message': 'cart not found'})
    cart.status = 'checkout'
    db.session.commit()

    if send_email([current_user.email], 'Cart created',
                  f''' Your cart has been created. You will be notified when your cart is ready to be picked up.'''):
        return jsonify({'success': True, 'message': 'Cart checked out successfully'})
    else:
        return jsonify({'success': True, 'message': 'Cart checked out no email sent'})

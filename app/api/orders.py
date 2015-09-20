from flask import jsonify
from flask.ext.login import current_user
from . import api
from ..models import Order

@api.route('/orders')
def get_orders():
    orders = Order.query.all()
    return jsonify({'orders':[i.serialize for i in orders]})

@api.route('/orders/<int:id>')
def get_order(id):
    order = Order.query.get(id)
    return jsonify(order.serialize)
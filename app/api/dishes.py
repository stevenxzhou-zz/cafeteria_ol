from flask import jsonify
from flask.ext.login import current_user
from . import api
from ..models import Dish

@api.route('/dishes')
def get_dishes():
    dishes = Dish.query.all()
    return jsonify({'dishes':[i.serialize for i in dishes]})

@api.route('/dishes/<int:id>')
def get_dish(id):
    dish = Dish.query.get(id)
    return jsonify(dish.serialize)
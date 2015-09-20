from flask import jsonify
from flask.ext.login import current_user
from . import api
from ..models import Store

@api.route('/stores')
def get_stores():
    stores = Store.query.all()
    return jsonify({'stores':[i.serialize for i in stores]})

@api.route('/stores/<int:id>')
def get_store(id):
    store = Store.query.get(id)
    return jsonify(store.serialize)
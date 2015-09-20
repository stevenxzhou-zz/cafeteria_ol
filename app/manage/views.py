from flask import render_template, jsonify, flash, url_for, redirect, request
from . import manage
from .. import db
from ..models import Store, Dish, Order, User
from .forms import StateUpdateForm
from flask.ext.login import current_user, login_required
from datetime import datetime

@manage.route('/update-orders', methods=['GET','POST'])
def update_orders():
    print(123)
    form = StateUpdateForm()
    state = request.form['state']
    orderid = request.form['orderid']
    update_order = Order.query.filter_by(id=orderid).first()
    if state == '2':
        update_order.state = 2
        db.session.commit()
    elif state == '1':
        update_order.state = 1
        db.session.commit()
    flash('Orders has been updated!')
    return "success"

@manage.route('/update-missed', methods=['GET','POST'])
def update_missed():
    Orders = Order.query.all()
    now = datetime.now()
    for order in Orders:
        if(order.date < now and order.state == 1):
            order.state=3
            db.session.commit()
    return "success"
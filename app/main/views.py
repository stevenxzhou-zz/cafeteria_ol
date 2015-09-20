from flask import render_template, jsonify, flash, url_for, redirect, request
from flask import json as json2
from . import main
from .. import db
from ..models import Store
from ..models import Dish
from ..models import Order, User
from .forms import TimePickerForm, StateUpdateForm
from flask.ext.login import current_user, login_required
from datetime import datetime

@main.route('/')
@login_required
def index():
    timeform = TimePickerForm()
    stores = Store.query.all()
    stores_json = jsonify({'stores':[i.serialize for i in stores]})
    dishes = Dish.query.all()
    return render_template('index.html', stores=stores, stores_json=stores_json, dishes=dishes, timeform=timeform)

@main.route('/manage')
@login_required
def manage():
    form = StateUpdateForm()
    if current_user.role_id == 2:
        orders = db.session.query(Order).join(Store, Store.id == Order.store_id).join(Dish, Dish.id == Order.dish_id).join(User, User.id == Order.user_id).order_by(Order.date.asc())
        #orders = Order.query.all()
        return render_template('manage/manage.html', orders = orders, form=form, current_time=datetime.utcnow())
    else:
        return "Unauthorized User."

@main.route('/submit-order', methods=['GET','POST'])
def submit_order():
    form = TimePickerForm()
    if (form.validate_on_submit()):
        new_order = Order(store_id = form.storeid.data, dish_id =form.dishid.data, user_id = current_user.id, date = form.time.data, state=True)
		#state = True # 1: unprocessed 2: processed 0: missed 
        db.session.add(new_order)
        db.session.commit()
        flash('New order has been added!')
        return redirect(url_for('main.index'))
    timeform = TimePickerForm()
    stores = Store.query.all()
    stores_json = jsonify({'stores':[i.serialize for i in stores]})
    dishes = Dish.query.all()
    return render_template('index.html', stores=stores, stores_json=stores_json, dishes=dishes, timeform=timeform)

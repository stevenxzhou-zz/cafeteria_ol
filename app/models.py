from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    orders = db.relationship('Order', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    storename = db.Column(db.String(64), unique=True, index=True)
    dishes = db.relationship('Dish', backref='store', lazy='dynamic')
    orders = db.relationship('Order', backref='store', lazy='dynamic')

    def __init__(self, storename):
        self.storename = storename

    @property
    def serialize(self):
        return {
            'id'        :self.id,
            'storename' :self.storename
        }
    
    def __repr_(self):
        return '<Store %r>' % self.storename

    

    
class Dish(db.Model):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    dishname =  db.Column(db.String(64), unique=True, index=True)
    dishprice = db.Column(db.Numeric)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    orders = db.relationship('Order', backref='dish', lazy='dynamic')
    
    @property
    def serialize(self):
        return {
            'id'        :self.id,
            'dishname'  :self.dishname,
            'price'     :round(self.dishprice,2),
            'store_id'  :self.store_id
    }

    def __repr_(self):
        return '<Dish %r>' % self.dishname

    
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    state = db.Column(db.Integer)
    @property
    def serialize(self):
        return {
            'id'        :self.id,
            'store_id'  :self.store_id,
            'user_id'   :self.user_id,
            'quantity'  :self.quantity,
            'date'      :self.date,
            'state'     :self.state
    }
    def __repr_(self):
        return '<Order %r>' % self.id

class ShopOwner(db.Model):
    __tablename__ = 'shopowners'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

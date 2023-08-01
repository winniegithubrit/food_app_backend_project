from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.orm import validates
from marshmallow import Schema, fields

db = SQLAlchemy()


class Owner(db.Model):
    __tablename__ = 'owner'
    owner_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    image = db.Column(db.String)

    locations = db.relationship('Location', backref='owner')
    restaurant_listing = db.relationship('Restaurant', backref='owner')

class Location(db.Model):
    __tablename__ = 'location'
    location_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, ForeignKey('owner.owner_id'))
    name = db.Column(db.String)

    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.restaurant_id'))
    restaurant = db.relationship('Restaurant', backref='location')


class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, ForeignKey('menu.menu_id'))
    customer_id = db.Column(db.Integer, ForeignKey('customers.customer_id'))
    # item_list = db.Column(db.String)
    total_price = db.Column(db.Integer)
    order_date_and_time = db.Column(db.DateTime)
    address = db.Column(db.String)
    # instructions = db.Column(db.String)
    payment_method = db.Column(db.String)
    # order_status = db.Column(db.String)

    deliveries = db.relationship('Deliveries', backref='order')

class Driver(db.Model):
    __tablename__ = 'driver'
    driver_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    phone_number = db.Column(db.String)
    image = db.Column(db.String)

    deliveries = db.relationship('Deliveries', backref='driver')


class Deliveries(db.Model):
    __tablename__ = 'deliveries'
    delivery_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey('order.order_id')) 
    driver_id = db.Column(db.Integer, ForeignKey('driver.driver_id'))
    delivery_date_and_time = db.Column(db.DateTime)
    dispatch = db.Column(db.Boolean, default=False)
    delivered = db.Column(db.Boolean, default=False)  
  
    
class Payment(db.Model):
    __tablename__ = 'payment'
    payment_id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.restaurant_id'))
    payment_type = db.Column(db.String)
    payment_amount = db.Column(db.Integer)
    payment_date_and_time = db.Column(db.DateTime)
    payment_status = db.Column(db.String)

class Customers(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    password = db.Column(db.String)
    phone_number = db.Column(db.String)
    image = db.Column(db.String)

    orders = db.relationship('Order', backref='customer')
    reviews = db.relationship('Reviews', backref='customer')

class Reviews(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, ForeignKey('customers.customer_id'))
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.restaurant_id'))
    rating = db.Column(db.Integer)
    review_comment = db.Column(db.String)
    review_date = db.Column(db.DateTime)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    restaurant_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer,ForeignKey('owner.owner_id'))
    restaurant_name = db.Column(db.String)
    contact_number = db.Column(db.String)
    opening_hours = db.Column(db.Time)
    closing_hours = db.Column(db.Time)
    # delivery_fee = db.Column(db.Integer)
    image = db.Column(db.String)
    payment_method = db.Column(db.String)
    
   
    menus = db.relationship('Menu', backref='restaurant')
    owner = db.relationship('Owner', backref='restaurant_listing')



class Menu(db.Model):
    __tablename__ = 'menu'
    menu_id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.restaurant_id'))
    menu_name = db.Column(db.String)
    description = db.Column(db.String)
    prices = db.Column(db.Integer)

class Users(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    type = db.Column(db.Boolean, default=False)  
    blocked = db.Column(db.String)
    activity = db.Column(db.String)

class Favourites(db.Model):
    __tablename__ ='favourite'
    favourite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'))
    menu_id = db.Column(db.Integer, ForeignKey('menu.menu_id'))

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, ForeignKey('customers.customer_id'))
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.restaurant_id'))
    owner_id = db.Column(db.Integer, ForeignKey('owner.owner_id'))
    name = db.Column(db.String)
    password = db.Column(db.String)
    
class SuperAdmin(db.Model):
    __tablename__ = 'superadmin'
    superadmin_id_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, ForeignKey('customers.customer_id'))
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.restaurant_id'))
    owner_id = db.Column(db.Integer, ForeignKey('owner.owner_id'))
    name = db.Column(db.String)
    password = db.Column(db.String)
    
    @validates("password")
    def validate_password(self, key, password):
        if password and len(password) > 100:
            raise ValueError('User password is not valid, please try again')
        return password

class OwnerSchema(Schema):
    owner_id = fields.Integer()
    name = fields.String()
    email = fields.String()
    password = fields.String()
    image = fields.String()

class LocationSchema(Schema):
    location_id = fields.Integer()
    owner_id = fields.Integer()
    name = fields.String()

class OrderSchema(Schema):
    order_id = fields.Integer()
    menu_id = fields.Integer(dump_only=True)
    customer_id = fields.Integer()
    item_list = fields.String()
    total_price = fields.Integer()
    order_date_and_time = fields.DateTime()
    address = fields.String()
    instructions = fields.String()
    payment_method = fields.String()
    order_status = fields.String()

class DriverSchema(Schema):
    driver_id = fields.Integer()
    name = fields.String()
    email = fields.String()
    password = fields.String()
    phone_number = fields.String()
    image = fields.String()


class DeliveriesSchema(Schema):
    delivery_id = fields.Integer()
    driver_id = fields.Integer()
    delivery_date_and_time = fields.DateTime()
    dispatch = fields.String()
    delivered = fields.String()

class PaymentSchema(Schema):
    payment_id = fields.Integer()
    order_id = fields.Integer()
    payment_amount = fields.Integer()
    payment_date_and_time = fields.DateTime()
    payment_status = fields.String()

class AnalyticsSchema(Schema):
    analytics_id = fields.Integer()
    restaurant_id = fields.Integer()
    performance = fields.String()

class CustomersSchema(Schema):
    customer_id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    password = fields.String()
    phone_number = fields.String()
    image = fields.String()

class ReviewsSchema(Schema):
    review_id = fields.Integer()
    customer_id = fields.Integer()
    restaurant_id = fields.Integer()
    rating = fields.Integer()
    review_comment = fields.String()
    review_date = fields.DateTime()

class MenuSchema(Schema):
    menu_id = fields.Integer()
    restaurant_id = fields.Integer()
    menu_name = fields.String()
    description = fields.String()
    prices = fields.Integer()
    
class RestaurantSchema(Schema):
    restaurant_id = fields.Integer()
    restaurant_name = fields.String()
    cuisine_type = fields.String()
    contact_number = fields.String()
    opening_hours = fields.Time()
    closing_hours = fields.Time()
    delivery_fee = fields.Integer()
    image = fields.String()
    payment_method = fields.String()
    menus = fields.Nested(MenuSchema, many=True)

class UsersSchema(Schema):
    user_id = fields.Integer()
    name = fields.String()
    email = fields.String()
    password = fields.String()
    user_type = fields.String()

class AdminSchema(Schema):
    admin_id = fields.Integer()
    customer_id = fields.Integer()
    restaurant_id = fields.Integer()
    owner_id = fields.Integer()
    name = fields.String()
    password = fields.String()
    
class SuperAdminSchema(Schema):
    superadmin_id = fields.Integer()
    customer_id = fields.Integer()
    restaurant_id = fields.Integer()
    owner_id = fields.Integer()
    name = fields.String()
    password = fields.String()

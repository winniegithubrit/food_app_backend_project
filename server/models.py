from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey 
# from sqlalchemy import func
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

class Location(db.Model):
    __tablename__ = 'location'
    location_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, ForeignKey('owner.owner_id'))
    name = db.Column(db.String)

class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.restaurant_id'))
    customer_id = db.Column(db.Integer, ForeignKey('customers.customer_id'))
    item_list = db.Column(db.String)
    total_price = db.Column(db.Integer)
    order_date_and_time = db.Column(db.DateTime)
    address = db.Column(db.String)
    instructions = db.Column(db.String)
    payment_method = db.Column(db.String)
    order_status = db.Column(db.String)

    deliveries = db.relationship('Deliveries', backref='order')
    payments = db.relationship('Payment', backref='order')

class Driver(db.Model):
    __tablename__ = 'driver'
    driver_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    phone_number = db.Column(db.Integer)
    image = db.Column(db.String)
    mode_of_transportation = db.Column(db.String)
    

    deliveries = db.relationship('Deliveries', backref='driver')

class Deliveries(db.Model):
    __tablename__ = 'deliveries'
    delivery_id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, ForeignKey('driver.driver_id'))
    order_id = db.Column(db.Integer, ForeignKey('order.order_id'))
    delivery_date_and_time = db.Column(db.DateTime)
    payment_status = db.Column(db.String)

class Payment(db.Model):
    __tablename__ = 'payment'
    payment_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey('order.order_id'))
    payment_amount = db.Column(db.Integer)
    payment_date_and_time = db.Column(db.DateTime)
    payment_status = db.Column(db.String)

class Analytics(db.Model):
    __tablename__ = 'analytics'
    analytics_id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.restaurant_id'))
    performance = db.Column(db.String)

class Customers(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String)
    phone_number = db.Column(db.Integer)
    image = db.Column(db.String)
    
    orders = db.relationship('Order', backref='customer')
    reviews = db.relationship('Reviews', backref='customer')
    admins = db.relationship('Admin', backref='customer')

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
    restaurant_name = db.Column(db.String)
    cuisine_type = db.Column(db.String)
    contact_number = db.Column(db.Integer)
    opening_hours = db.Column(db.Time)
    delivery_fee = db.Column(db.Integer)
    image = db.Column(db.String)
    payment_method = db.Column(db.String)

    orders = db.relationship('Order', backref='restaurant')
    analytics = db.relationship('Analytics', backref='restaurant')
    menus = db.relationship('Menu', backref='restaurant')
    admins = db.relationship('Admin', backref='restaurant')

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
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    profile = db.relationship('Profile', backref='user', uselist=False)
    
    @validates("password")
    def validate_password(self, key, password):
        if password and len(password) > 100:
            raise ValueError('User password is not valid, please try again')
        return password

class Profile(db.Model):
    __tablename__ = 'profile'
    profile_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    profile_picture = db.Column(db.String)
    location = db.Column(db.String)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'), unique=True)  

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
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
    restaurant_id = fields.Integer()
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
    phone_number = fields.Integer()
    image = fields.String()
    mode_of_transportation = fields.String()

class DeliveriesSchema(Schema):
    delivery_id = fields.Integer()
    driver_id = fields.Integer()
    order_id = fields.Integer()
    delivery_date_and_time = fields.DateTime()
    payment_status = fields.String()

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
    phone_number = fields.Integer()
    image = fields.String()

class ReviewsSchema(Schema):
    review_id = fields.Integer()
    customer_id = fields.Integer()
    restaurant_id = fields.Integer()
    rating = fields.Integer()
    review_comment = fields.String()
    review_date = fields.DateTime()

class RestaurantSchema(Schema):
    restaurant_id = fields.Integer()
    restaurant_name = fields.String()
    cuisine_type = fields.String()
    contact_number = fields.Integer()
    opening_hours = fields.Time()
    delivery_fee = fields.Integer()
    image = fields.String()
    payment_method = fields.String()

class MenuSchema(Schema):
    menu_id = fields.Integer()
    restaurant_id = fields.Integer()
    menu_name = fields.String()
    description = fields.String()
    prices = fields.Integer()
    
class ProfileSchema(Schema):
    profile_id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    profile_picture = fields.String()
    location = fields.String()
    user_id = fields.Integer()

class UsersSchema(Schema):
    user_id = fields.Integer()
    name = fields.String()
    email = fields.String()
    password = fields.String()
    profile = fields.Nested(ProfileSchema) 



class AdminSchema(Schema):
    admin_id = fields.Integer()
    customer_id = fields.Integer()
    restaurant_id = fields.Integer()
    owner_id = fields.Integer()
    name = fields.String()
    password = fields.String()


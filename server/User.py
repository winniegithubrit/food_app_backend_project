from flask import Blueprint, jsonify,request
from flask_marshmallow import Marshmallow
from models import User,db,Customers,Driver

user = Blueprint("User", __name__)
ma = Marshmallow(user)

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customers
        customer_id = ma.auto_field()
        user_id = ma.auto_field()
        user_name = ma.auto_field()
        password = ma.auto_field()
        phone_number = ma.auto_field()
        image = ma.auto_field()

@user.route('/')
def index():
    return "User Page"

# CUSTOMERS
@user.route('/customers', methods=['GET'])
def get_all_customers():
    customers = Customers.query.all()
    customer_schema = CustomerSchema(many=True)
    customer_data = customer_schema.dump(customers)
    return jsonify(customer_data)

@user.route('/customers/<int:customer_id>', methods=['GET'])
def get_customers_by_id(customer_id):
    customer = Customers.query.get(customer_id)
    if customer is None:
        return jsonify({'message': 'Customer not found'}), 404
    customer_schema = CustomerSchema()
    customer_data = customer_schema.dump(customer)
    return jsonify(customer_data)
  

@user.route('/customers', methods=['POST'])
def create_customers():
    data = request.get_json()

    customer_schema = CustomerSchema()
    customers = customer_schema.load(data)

    new_customer = Customers(**customers)

    db.session.add(new_customer)
    db.session.commit()

    customer_data = customer_schema.dump(new_customer)
    return jsonify(customer_data), 201
  

@user.route('/customers/<int:customer_id>', methods=['PATCH'])
def update_customer(customer_id):
    data = request.get_json()

    customers = Customers.query.filter_by(customer_id=customer_id).first()
    if not customers:
        return jsonify({'message': "The customer you are looking for is not found"}), 404

    customer_schema = CustomerSchema()
    updated_customer_data = customer_schema.load(data, partial=True)

    for key, value in updated_customer_data.get('customers', {}).items():
        setattr(customers, key, value)

    db.session.commit()
    customer_data = customer_schema.dump(customers)
    return jsonify(customer_data)


@user.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customers = Customers.query.filter_by(customer_id=customer_id).first()
    if not customers:
        return jsonify({'message': 'Customers not found'}), 404

    db.session.delete(customers)
    db.session.commit()

    return jsonify({'message': 'Customer deleted succesfully'}), 204


# DRIVER

class DriverSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Driver
        driver_id = ma.auto_field()
        name = ma.auto_field()
        email = ma.auto_field()
        password = ma.auto_field()
        phone_number = ma.auto_field()
        image = ma.auto_field()
        current = ma.auto_field()
        
@user.route('/driver', methods=['GET'])
def get_all_drivers():
    driver = Driver.query.all()
    driver_schema = DriverSchema(many=True)
    driver_data = driver_schema.dump(driver)
    return jsonify(driver_data)


@user.route('/driver/<int:driver_id>', methods=['GET'])
def get_driver_by_id(driver_id):
    driver = Driver.query.get(driver_id)
    if driver is None:
        return jsonify({'message': 'Driver not found'}), 404
    driver_schema = DriverSchema()
    driver_data = driver_schema.dump(driver)
    return jsonify(driver_data)


@user.route('/driver', methods=['POST'])
def create_drivers():
    data = request.get_json()

    driver_schema = DriverSchema()
    driver = driver_schema.load(data)

    new_driver = Driver(**driver)

    db.session.add(new_driver)
    db.session.commit()

    driver_data = driver_schema.dump(new_driver)
    return jsonify(driver_data), 201

@user.route('/driver/<int:driver_id>', methods=['PATCH'])
def update_driver(driver_id):
    data = request.get_json()

    driver = Driver.query.filter_by(driver_id=driver_id).first()
    if not driver:
        return jsonify({'message': "The driver you are looking for is not found"}), 404

    driver_schema = DriverSchema()
    updated_driver_data = driver_schema.load(data, partial=True)

    for key, value in updated_driver_data.get('driver', {}).items():
        setattr(driver, key, value)

    db.session.commit()
    driver_data = driver_schema
    
@user.route('/driver/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    driver = Driver.query.filter_by(driver_id=driver_id).first()
    if not driver:
        return jsonify({'message': 'Driver not found'}), 404

    db.session.delete(driver)
    db.session.commit()

    return jsonify({'message': 'Driver deleted succesfully'}), 204

# USER

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        user_id = ma.auto_field()
        user_name  = ma.auto_field()
        email = ma.auto_field()
        password = ma.auto_field()
        type = ma.auto_field()
        blocked = ma.auto_field()
        activity = ma.auto_field()
        
@user.route('/users', methods=['GET'])
def get_all_users():
    user = User.query.all()
    user_schema = UserSchema(many=True)
    user_data = user_schema.dump(user)
    return jsonify(user_data)

@user.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    user_schema = UserSchema()
    user_data = user_schema.dump(user)
    return jsonify(user_data)


@user.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    user_schema = UserSchema()
    user = user_schema.load(data)

    new_user = User(**user)

    db.session.add(new_user)
    db.session.commit()

    user_data = user_schema.dump(new_user)
    return jsonify(user_data), 201

@user.route('/user/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.get_json()

    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'message': "The user you are looking for is not found"}), 404

    user_schema = UserSchema()
    updated_user_data = user_schema.load(data, partial=True)

    for key, value in updated_user_data.get('user', {}).items():
        setattr(user, key, value)

    db.session.commit()
    user_data = user_schema
    
@user.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted succesfully'}), 204

# ADMIN
class AdminSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Admin
        owner_id = ma.auto_field()
        name = ma.auto_field()
        email = ma.auto_field()
        password = ma.auto_field()
        image = ma.auto_field()
        
@user.route('/admin', methods=['GET'])
def get_all_admin():
    admin = Admin.query.all()
    admin_schema = AdminSchema(many=True)
    admin_data = admin_schema.dump(admin)
    return jsonify(admin_data)


        
    



from flask import Blueprint, jsonify,Flask,request,make_response
from flask_marshmallow import Marshmallow
from models import Restaurant,db,Menu,Order,Payment
# from marshmallow import Schema, fields

restaurants = Blueprint("restaurants", __name__)
ma = Marshmallow()

class RestaurantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Restaurant 
        restaurant_name = ma.auto_field()
        cuisine_type = ma.auto_field()
        contact_number = ma.auto_field()
        opening_hours = ma.auto_field()
        closing_hours = ma.auto_field()
        delivery_fee = ma.auto_field()
        image = ma.auto_field()
        payment_method = ma.auto_field()

app = Flask(__name__)
ma.init_app(app)

@restaurants.route('/')
def index():
    return "This is the Products page"

# RESTAURANTS
@restaurants.route('/restaurants', methods=['GET'])
def get_all_restaurants():
    restaurants_list = Restaurant.query.all()
    restaurant_schema = RestaurantSchema(many=True)
    restaurant_data = restaurant_schema.dump(restaurants_list)  
    return jsonify(restaurant_data)
  
@restaurants.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.filter_by(restaurant_id=restaurant_id).first()
    if restaurant is None:
        return jsonify({'message': 'Restaurant is not found'}), 404

    restaurant_schema = RestaurantSchema()
    restaurant_data = restaurant_schema.dump(restaurant)
    return jsonify(restaurant_data)
  
@restaurants.route('/restaurants', methods=['POST'])
def create_restaurants():
    data = request.get_json()

    restaurant_schema = RestaurantSchema()
    restaurant = restaurant_schema.load(data)

    new_restaurant = Restaurant(**restaurant)

    db.session.add(new_restaurant)
    db.session.commit()

    restaurant_data = restaurant_schema.dump(new_restaurant)
    return jsonify(restaurant_data), 201

@restaurants.route('/restaurants/<int:restaurant_id>', methods=['PATCH'])
def update_restaurant(restaurant_id):
    data = request.get_json()

    restaurant = Restaurant.query.filter_by(restaurant_id=restaurant_id).first()
    if not restaurant:
        return jsonify({'message': "The restaurant you are looking for is not found"}), 404

    restaurant_schema = RestaurantSchema()
    updated_restaurant_data = restaurant_schema.load(data, partial=True)

    for key, value in updated_restaurant_data.get('restaurant', {}).items():
        setattr(restaurant, key, value)

    db.session.commit()
    restaurant_data = restaurant_schema.dump(restaurant)
    return jsonify(restaurant_data)


@restaurants.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.filter_by(restaurant_id=restaurant_id).first()
    if not restaurant:
        return jsonify({'message': 'Restaurant not found'}), 404

    db.session.delete(restaurant)
    db.session.commit()

    return jsonify({'message': 'Restaurant deleted succesfully'}), 204

# MENUS

class MenuSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Menu
        menu_id = ma.auto_field()
        restaurant_id = ma.auto_field()
        menu_name = ma.auto_field()
        description = ma.auto_field()
        prices = ma.auto_field()
        
@restaurants.route('/menus', methods=['GET'])
def get_all_menus():
    menu_list = Menu.query.all()
    menu_schema = MenuSchema(many=True)
    menu_data = menu_schema.dump(menu_list)  
    return jsonify(menu_data)


@restaurants.route('/menus/<int:menu_id>', methods=['GET'])
def get_menu(menu_id):
    menu = Menu.query.filter_by(menu_id=menu_id).first()
    if menu is None:
        return jsonify({'message': 'Menu is not found'}), 404

    menu_schema = MenuSchema()
    menu_data = menu_schema.dump(menu)
    return jsonify(menu_data)

@restaurants.route('/menus', methods=['POST'])
def create_menus():
    data = request.get_json()

    menu_schema = MenuSchema()
    menu = menu_schema.load(data)

    new_menu = Menu(**menu)

    db.session.add(new_menu)
    db.session.commit()

    menu_data = menu_schema.dump(new_menu)
    return jsonify(menu_data), 201

@restaurants.route('/menus/<int:menu_id>', methods=['PATCH'])
def update_menu(menu_id):
    data = request.get_json()

    menu = Menu.query.filter_by(menu_id=menu_id).first()
    if not menu:
        return jsonify({'message': "The menu you are looking for is not found"}), 404

    menu_schema = MenuSchema()
    updated_menu_data = menu_schema.load(data, partial=True)

    for key, value in updated_menu_data.get('menu', {}).items():
        setattr(menu, key, value)

    db.session.commit()
    menu_data = menu_schema.dump(menu)
    return jsonify(menu_data)



@restaurants.route('/menus/<int:menu_id>', methods=['DELETE'])
def delete_menu(menu_id):
    menu = Menu.query.filter_by(menu_id=menu_id).first()
    if not menu:
        return jsonify({'message': 'Menu not found'}), 404

    db.session.delete(menu)
    db.session.commit()

    return jsonify({'message': 'Menu deleted succesfully'}), 204


# ORDERS

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        order_id = ma.auto_field()
        menu_id = ma.auto_field()
        total_price = ma.auto_field()
        order_date_and_time = ma.auto_field()
        address = ma.auto_field()
        payment_method = ma.auto_field()
        


@restaurants.route('/orders', methods=['GET'])
def get_all_orders():
    order_list = Order.query.all()
    order_schema = OrderSchema(many=True)
    order_data = order_schema.dump(order_list)  
    return jsonify(order_data)


@restaurants.route('/orders/<int:order_id>', methods=['GET'])
def get_orders(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if order is None:
        return jsonify({'message': 'Orders are not found'}), 404

    order_schema = OrderSchema()
    order_data = order_schema.dump(order)
    return jsonify(order_data)


@restaurants.route('/orders', methods=['POST'])
def create_orders():
    data = request.get_json()

    order_schema = OrderSchema()
    order = order_schema.load(data)

    new_order = Order(**order)

    db.session.add(new_order)
    db.session.commit()

    order_data = order_schema.dump(new_order)
    return jsonify(order_data), 201


@restaurants.route('/orders/<int:order_id>', methods=['PATCH'])
def update_order(order_id):
    data = request.get_json()

    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        return jsonify({'message': "The order you are looking for is not found"}), 404

    order_schema = OrderSchema()
    updated_order_data = order_schema.load(data, partial=True)

    for key, value in updated_order_data.get('order', {}).items():
        setattr(order, key, value)

    db.session.commit()
    order_data = order_schema.dump(order)
    return jsonify(order_data)



@restaurants.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({'message': 'Order deleted succesfully'}), 204

# PAYMENT

class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Payment
        payment_id = ma.auto_field()
        restaurant_id =  ma.auto_field()
        payment_type =  ma.auto_field()
        payment_amount =  ma.auto_field()
        payment_date_and_time =  ma.auto_field()
        payment_status =  ma.auto_field()
        
@restaurants.route('/payment', methods=['GET'])
def get_all_payments():
    payment_list = Payment.query.all()
    payment_schema = PaymentSchema(many=True)
    payment_data = payment_schema.dump(payment_list)  
    return jsonify(payment_data)


@restaurants.route('/payment/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = Payment.query.filter_by(payment_id=payment_id).first()
    if payment is None:
        return jsonify({'message': 'Payments are not found'}), 404

    payment_schema = PaymentSchema()
    payment_data = payment_schema.dump(payment)
    return jsonify(payment_data)

@restaurants.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    payment = PaymentSchema().load(data)
    new_payment = Payment(**payment)
    db.session.add(new_payment)
    db.session.commit()
    payment_data = PaymentSchema().dump(new_payment)
    return make_response(jsonify(payment_data), 201)


@restaurants.route('/payment/<int:payment_id>', methods=['PATCH'])
def update_payment_details(payment_id):
    payment = Payment.query.filter_by(payment_id=payment_id).first()
    data = request.get_json()
    payment = PaymentSchema().load(data)
    for field, value in data.items():  
        setattr(payment, field, value)
    db.session.add(payment)
    db.session.commit()

    payment_data = PaymentSchema().dump(payment)
    return make_response(jsonify(payment_data))



@restaurants.route('/payment/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    payment = Payment.query.filter_by(payment_id=payment_id).first()
    if not payment:
        return jsonify({'message': 'Payment not found'}), 404

    db.session.delete(payment)
    db.session.commit()

    return jsonify({'message': 'Payment deleted succesfully'}), 204





















        


  
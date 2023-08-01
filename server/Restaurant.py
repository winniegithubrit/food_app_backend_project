from flask import Blueprint, jsonify,Flask,request
from flask_marshmallow import Marshmallow
from models import Restaurant,db

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
def create_restaurant(restaurant_id):
  data = request.get_json()
  
  restaurant = Restaurant.query.filter_by(restaurant_id=restaurant_id).first()
  if not restaurant:
    return jsonify({'message':"the restaurant you are looking for is not found"}), 404
  restaurant_schema = RestaurantSchema()
  updated_restaurant_data = restaurant_schema.load(data,partial=True)
  
  restaurant.restaurant_name = updated_restaurant_data.get('restaurant', restaurant.restaurant_name)
  restaurant.cuisine_type = updated_restaurant_data.get('restaurant', restaurant.cuisine_type)
  restaurant.contact_number = updated_restaurant_data.get('restaurant', restaurant.contact_number)
  restaurant.opening_hours = updated_restaurant_data.get('restaurant', restaurant.opening_hours)
  restaurant.delivery_fee = updated_restaurant_data.get('restaurant', restaurant.delivery_)
  db.session.commit()
  restaurant_data = restaurant_schema.dump(restaurant)
  return jsonify(restaurant_data)
  
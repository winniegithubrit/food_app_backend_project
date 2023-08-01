from flask import Blueprint, jsonify,Flask
from flask_marshmallow import Marshmallow
from models import Restaurant

restaurants = Blueprint("restaurants", __name__)
ma = Marshmallow()

class RestaurantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Restaurant 

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
  
@app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.filter_by(restaurant_id=restaurant_id).first()
    if restaurant is None:
        return jsonify({'message': 'Restaurant is not found'}), 404

    restaurant_schema = RestaurantSchema()
    restaurant_data = restaurant_schema.dump(restaurant)
    return jsonify(restaurant_data)


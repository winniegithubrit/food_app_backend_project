from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

restaurants = Blueprint("Restaurant", __name__)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(100), nullable=False)
    cuisine_type = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    opening_hours = db.Column(db.String(100), nullable=False)
    delivery_fee = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200))
    payment_method = db.Column(db.String(100))

    def __init__(self, restaurant_name, cuisine_type, contact_number, opening_hours, delivery_fee, image=None, payment_method=None):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type
        self.contact_number = contact_number
        self.opening_hours = opening_hours
        self.delivery_fee = delivery_fee
        self.image = image
        self.payment_method = payment_method


class RestaurantSchema(Schema):
    class Meta:
        fields = ('id', 'restaurant_name', 'cuisine_type', 'contact_number', 'opening_hours', 'delivery_fee', 'image', 'payment_method')


restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)


@restaurants.route('/restaurants', methods=['GET'])
def get_all_restaurants():
    all_restaurants = Restaurant.query.all()
    result = restaurants_schema.dump(all_restaurants)
    return jsonify(result), 200


@restaurants.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return restaurant_schema.jsonify(restaurant), 200
    else:
        return jsonify({'message': 'Restaurant not found'}), 404


@restaurants.route('/restaurants', methods=['POST'])
def create_restaurant():
    data = request.json
    new_restaurant = Restaurant(restaurant_name=data['restaurant_name'],
                                cuisine_type=data['cuisine_type'],
                                contact_number=data['contact_number'],
                                opening_hours=data['opening_hours'],
                                delivery_fee=data['delivery_fee'],
                                image=data.get('image'),
                                payment_method=data.get('payment_method'))

    db.session.add(new_restaurant)
    db.session.commit()

    return restaurant_schema.jsonify(new_restaurant), 201


@restaurants.route('/restaurants/<int:id>', methods=['PATCH', 'PUT'])
def update_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({'message': 'Restaurant not found'}), 404

    data = request.json
    restaurant.restaurant_name = data['restaurant_name']
    restaurant.cuisine_type = data['cuisine_type']
    restaurant.contact_number = data['contact_number']
    restaurant.opening_hours = data['opening_hours']
    restaurant.delivery_fee = data['delivery_fee']
    restaurant.image = data.get('image')
    restaurant.payment_method = data.get('payment_method')

    db.session.commit()

    return restaurant_schema.jsonify(restaurant), 200


@restaurants.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({'message': 'Restaurant not found'}), 404

    db.session.delete(restaurant)
    db.session.commit()

    return jsonify({'message': 'Restaurant deleted successfully'}), 200


if __name__ == '__main__':
    db.create_all()
    app.register_blueprint(restaurants, url_prefix='/restaurants')
    app.run(debug=True)

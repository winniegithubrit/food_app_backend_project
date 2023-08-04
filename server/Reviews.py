from flask import Flask,Blueprint,jsonify,request,make_response
from flask_marshmallow import Marshmallow
from models import db,CustomerReviews,RestaurantReviews,MenuReviews
reviews = Blueprint("Reviews",__name__)
ma = Marshmallow()

class CustomerReviewsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerReviews
        customerReview_id = ma.auto_field()
        customer_id = ma.auto_field()
        rating = ma.auto_field()
        review_comment = ma.auto_field()
        review_date = ma.auto_field()
        

app = Flask(__name__)
ma.init_app(app)


# CUSTOMER REVIEWS
# Endpoint to get all customer reviews
@reviews.route('/customerReviews', methods=['GET'])
def get_all_customer_reviews():
    customer_reviews_list = CustomerReviews.query.all()
    customer_reviews_schema = CustomerReviewsSchema(many=True)
    customer_reviews_data = customer_reviews_schema.dump(customer_reviews_list)  
    return jsonify(customer_reviews_data)

# Endpoint to get a specific customer review by ID
@reviews.route('/customerReviews/<int:review_id>', methods=['GET'])
def get_customer_review(review_id):
    customer_review = CustomerReviews.query.get(review_id)
    if customer_review is None:
        return jsonify({'message': 'Customer review not found'}), 404

    customer_review_schema = CustomerReviewsSchema()
    customer_review_data = customer_review_schema.dump(customer_review)
    return jsonify(customer_review_data)

# Endpoint to create a new customer review
@reviews.route('/customerReviews', methods=['POST'])
def create_customer_review():
    data = request.get_json()
    customer_review = CustomerReviewsSchema().load(data)
    new_customer_review = CustomerReviews(**customer_review)
    db.session.add(new_customer_review)
    db.session.commit()
    customer_review_data = CustomerReviewsSchema().dump(new_customer_review)
    return make_response(jsonify(customer_review_data), 201)

# Endpoint to update a customer review
@reviews.route('/customerReviews/<int:review_id>', methods=['PATCH'])
def update_customer_review(review_id):
    customer_review = CustomerReviews.query.get(review_id)
    if customer_review is None:
        return jsonify({'message': 'Customer review not found'}), 404

    data = request.get_json()
    customer_review = CustomerReviewsSchema().load(data)

    for field, value in data.items():  
        setattr(customer_review, field, value)

    db.session.commit()
    customer_review_data = CustomerReviewsSchema().dump(customer_review)
    return make_response(jsonify(customer_review_data))

# Endpoint to delete a customer review
@reviews.route('/customerReviews/<int:review_id>', methods=['DELETE'])
def delete_customer_review(review_id):
    customer_review = CustomerReviews.query.get(review_id)
    if not customer_review:
        return jsonify({'message': 'Customer review not found'}), 404

    db.session.delete(customer_review)
    db.session.commit()

    return jsonify({'message': 'Customer review deleted successfully'}), 204
  # RESTAURANT_REVIEWS
class RestaurantReviewsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RestaurantReviews
        restaurantReview_id = ma.auto_field()
        restaurant_id = ma.auto_field()
        rating = ma.auto_field()
        review_comment = ma.auto_field()
        review_date = ma.auto_field()
        
  
# Endpoint to get all restaurant reviews
@reviews.route('/restaurantReviews', methods=['GET'])
def get_all_restaurant_reviews():
    restaurant_reviews_list = RestaurantReviews.query.all()
    restaurant_reviews_schema = RestaurantReviewsSchema(many=True)
    restaurant_reviews_data = restaurant_reviews_schema.dump(restaurant_reviews_list)  
    return jsonify(restaurant_reviews_data)

# Endpoint to get a specific restaurant review by ID
@reviews.route('/restaurantReviews/<int:review_id>', methods=['GET'])
def get_restaurant_review(review_id):
    restaurant_review = RestaurantReviews.query.get(review_id)
    if restaurant_review is None:
        return jsonify({'message': 'Restaurant review not found'}), 404

    restaurant_review_schema = RestaurantReviewsSchema()
    restaurant_review_data = restaurant_review_schema.dump(restaurant_review)
    return jsonify(restaurant_review_data)

# Endpoint to create a new restaurant review
@reviews.route('/restaurantReviews', methods=['POST'])
def create_restaurant_review():
    data = request.get_json()
    restaurant_review = RestaurantReviewsSchema().load(data)
    new_restaurant_review = RestaurantReviews(**restaurant_review)
    db.session.add(new_restaurant_review)
    db.session.commit()
    restaurant_review_data = RestaurantReviewsSchema().dump(new_restaurant_review)
    return make_response(jsonify(restaurant_review_data), 201)

# Endpoint to update a restaurant review
@reviews.route('/restaurantReviews/<int:review_id>', methods=['PATCH'])
def update_restaurant_review(review_id):
    restaurant_review = RestaurantReviews.query.get(review_id)
    if restaurant_review is None:
        return jsonify({'message': 'Restaurant review not found'}), 404

    data = request.get_json()
    restaurant_review = RestaurantReviewsSchema().load(data)

    for field, value in data.items():  
        setattr(restaurant_review, field, value)

    db.session.commit()
    restaurant_review_data = RestaurantReviewsSchema().dump(restaurant_review)
    return make_response(jsonify(restaurant_review_data))

# Endpoint to delete a restaurant review
@reviews.route('/restaurantReviews/<int:review_id>', methods=['DELETE'])
def delete_restaurant_review(review_id):
    restaurant_review = RestaurantReviews.query.get(review_id)
    if not restaurant_review:
        return jsonify({'message': 'Restaurant review not found'}), 404

    db.session.delete(restaurant_review)
    db.session.commit()

    return jsonify({'message': 'Restaurant review deleted successfully'}), 204
  
# MENU REVIEWS
class MenuReviewsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MenuReviews
        menuReview_id = ma.auto_field()
        menu_id = ma.auto_field()
        rating = ma.auto_field()
        review_comment = ma.auto_field()
        review_date = ma.auto_field()
        
# Endpoint to get all menu reviews
@reviews.route('/menuReviews', methods=['GET'])
def get_all_menu_reviews():
    menu_reviews_list = MenuReviews.query.all()
    menu_reviews_schema = MenuReviewsSchema(many=True)
    menu_reviews_data = menu_reviews_schema.dump(menu_reviews_list)  
    return jsonify(menu_reviews_data)

# Endpoint to get a specific menu review by ID
@reviews.route('/menuReviews/<int:review_id>', methods=['GET'])
def get_menu_review(review_id):
    menu_review = MenuReviews.query.get(review_id)
    if menu_review is None:
        return jsonify({'message': 'Menu review not found'}), 404

    menu_review_schema = MenuReviewsSchema()
    menu_review_data = menu_review_schema.dump(menu_review)
    return jsonify(menu_review_data)

# Endpoint to create a new menu review
@reviews.route('/menuReviews', methods=['POST'])
def create_menu_review():
    data = request.get_json()
    menu_review = MenuReviewsSchema().load(data)
    new_menu_review = MenuReviews(**menu_review)
    db.session.add(new_menu_review)
    db.session.commit()
    menu_review_data = MenuReviewsSchema().dump(new_menu_review)
    return make_response(jsonify(menu_review_data), 201)

# Endpoint to update a menu review
@reviews.route('/menuReviews/<int:review_id>', methods=['PATCH'])
def update_menu_review(review_id):
    menu_review = MenuReviews.query.get(review_id)
    if menu_review is None:
        return jsonify({'message': 'Menu review not found'}), 404

    data = request.get_json()
    menu_review = MenuReviewsSchema().load(data)

    for field, value in data.items():  
        setattr(menu_review, field, value)

    db.session.commit()
    menu_review_data = MenuReviewsSchema().dump(menu_review)
    return make_response(jsonify(menu_review_data))

# Endpoint to delete a menu review
@reviews.route('/menuReviews/<int:review_id>', methods=['DELETE'])
def delete_menu_review(review_id):
    menu_review = MenuReviews.query.get(review_id)
    if not menu_review:
        return jsonify({'message': 'Menu review not found'}), 404

    db.session.delete(menu_review)
    db.session.commit()

    return jsonify({'message': 'Menu review deleted successfully'}), 204


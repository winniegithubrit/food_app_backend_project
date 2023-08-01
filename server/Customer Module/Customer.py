from flask import Blueprint,jsonify,Flask,request,session
from flask_marshmallow import Marshmallow
from models import Customers
customers = Blueprint("Customers",__name__)
ma = Marshmallow(customers)

class CustomerSchema(ma.SQLAlchemySchema):
  class Meta:
    model = customers
  customer_id = ma.auto_field()
  first_name = ma.auto_field()
  last_name = ma.auto_field()
  password = ma.auto_field()
  phone_number = ma.auto_field()
  image = ma.auto_field()

@customers.route('/')
def index():
  return "Customers Page"

# get all customers
@customers.route('/customers',methods=['GET'])
def get_all_customers():
  customers = Customers.query.all()
  customer_schema = CustomerSchema(many=True)
  customer_data = customer_schema.dump(customers)
  return jsonify(customer_data)

#get customer by id
@customers.route('/cutomers/<int:customer_id>',methods=['GET'])
def get_customers_by_id(customer_id):
  customeer = Customers.query.filter_by(customer_id=customer_id).first()
  if customeer is None:
    return jsonify({'message':'Customer has not been found'}), 404
  customer_schema = CustomerSchema()
  customer_data = customer_schema.dump(customers)
  return jsonify(customer_data)
  
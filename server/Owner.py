from flask import Blueprint,jsonify,Flask,request,make_response
from flask_marshmallow import Marshmallow
from schemas import *

from models import Owner,db,Deliveries,Location

owners = Blueprint("Owner",__name__)
ma = Marshmallow()


    
app = Flask(__name__)
ma.init_app(app)    

@owners.route('/')
def index():
    return "This is the Owner page"
  

# OWNERS
@owners.route('/owners', methods=['GET'])
def get_all_owners():
    owners_list = Owner.query.all()
    owner_schema = OwnerSchema(many=True)
    owner_data = owner_schema.dump(owners_list)  
    return jsonify(owner_data)
  
  
@owners.route('/owners/<int:owner_id>', methods=['GET'])
def get_owners(owner_id):
    owner = Owner.query.filter_by(owner_id=owner_id).first()
    if owner is None:
        return jsonify({'message': 'Owner is not found'}), 404

    owner_schema = OwnerSchema()
    owner_data = owner_schema.dump(owner)
    return jsonify(owner_data)
  
@owners.route('/owners', methods=['POST'])
def create_owners():
    data = request.get_json()
    owner = OwnerSchema().load(data)
    new_owner = Owner(**owner)
    db.session.add(new_owner)
    db.session.commit()
    owner_data = OwnerSchema().dump(new_owner)
    return make_response(jsonify(owner_data), 201)

@owners.route('/owners/<int:owner_id>', methods=['PATCH'])
def update_owners_details(owner_id):
    owner = Owner.query.filter_by(owner_id=owner_id).first()
    data = request.get_json()
    owners = OwnerSchema().load(data)
    for field, value in owners.items():  
        setattr(owner, field, value)
    db.session.add(owner)
    db.session.commit()

    owner_data = OwnerSchema().dump(owner)
    return make_response(jsonify(owner_data))

@owners.route('/owners/<int:owner_id>', methods=['DELETE'])
def delete_owner(owner_id):
    owner = Owner.query.filter_by(owner_id=owner_id).first()
    if not owner:
        return jsonify({'message': 'Owner not found'}), 404

    db.session.delete(owner)
    db.session.commit()

    return jsonify({'message': 'Owner deleted succesfully'}), 204


# DELIVERIES


@owners.route('/deliveries', methods=['GET'])
def get_all_deliveries():
    deliveries_list = Deliveries.query.all()
    deliveries_schema = DeliveriesSchema(many=True)
    deliveries_data = deliveries_schema.dump(deliveries_list)  
    return jsonify(deliveries_data)

@owners.route('/deliveries/<int:delivery_id>', methods=['GET'])
def get_deliveries(delivery_id):
    deliveries = Deliveries.query.filter_by(delivery_id=delivery_id).first()
    if deliveries is None:
        return jsonify({'message': 'Delivery is not found'}), 404

    deliveries_schema = DeliveriesSchema()
    deliveries_data = deliveries_schema.dump(deliveries)
    return jsonify(deliveries_data)

@owners.route('/deliveries', methods=['POST'])
def create_deliveries():
    data = request.get_json()
    deliveries = DeliveriesSchema().load(data)
    new_deliveries = Deliveries(**deliveries)
    db.session.add(new_deliveries)
    db.session.commit()
    deliveries_data = DeliveriesSchema().dump(new_deliveries)
    return make_response(jsonify(deliveries_data), 201)


@owners.route('/deliveries/<int:delivery_id>', methods=['PATCH'])
def update_deliveries_details(delivery_id):
    deliveries = Deliveries.query.filter_by(delivery_id=delivery_id).first()
    data = request.get_json()
    deliveriess = DeliveriesSchema().load(data)
    for field, value in deliveriess.items():  
        setattr(deliveries, field, value)
    db.session.add(deliveries)
    db.session.commit()

    deliveries_data = DeliveriesSchema().dump(deliveries)
    return make_response(jsonify(deliveries_data))


@owners.route('/delieries/<int:delivery_id>', methods=['DELETE'])
def delete_deliveries(delivery_id):
    deliveries = Deliveries.query.filter_by(delivery_id=delivery_id).first()
    if not deliveries:
        return jsonify({'message': 'Delivery not found'}), 404

    db.session.delete(deliveries)
    db.session.commit()

    return jsonify({'message': 'Delivery deleted succesfully'}), 204

# LOCATION 


    
    
@owners.route('/location', methods=['GET'])
def get_all_location():
    location_list = Location.query.all()
    location_schema = LocationSchema(many=True)
    location_data = location_schema.dump(location_list)  
    return jsonify(location_data)

@owners.route('/location/<int:location_id>', methods=['GET'])
def get_location(location_id):
    location = Location.query.filter_by(location_id=location_id).first()
    if location is None:
        return jsonify({'message': 'Location is not found'}), 404

    location_schema = LocationSchema()
    location_data = location_schema.dump(location)
    return jsonify(location_data)

@owners.route('/location', methods=['POST'])
def create_location():
    data = request.get_json()
    location = LocationSchema().load(data)
    new_location = Location(**location)
    db.session.add(new_location)
    db.session.commit()
    location_data = LocationSchema().dump(new_location)
    return make_response(jsonify(location_data), 201)


@owners.route('/location/<int:location_id>', methods=['PATCH'])
def update_location_details(location_id):
    location = Location.query.filter_by(location_id=location_id).first()
    data = request.get_json()
    location = LocationSchema().load(data)
    for field, value in data.items():  
        setattr(Location, field, value)
    db.session.add(location)
    db.session.commit()

    location_data = LocationSchema().dump(location)
    return make_response(jsonify(location_data))


@owners.route('/location/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    location = Location.query.filter_by(location_id=location_id).first()
    if not location:
        return jsonify({'message': 'Location not found'}), 404

    db.session.delete(location)
    db.session.commit()

    return jsonify({'message': 'Location deleted succesfully'}), 204


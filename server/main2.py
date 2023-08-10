#app.py
from flask import Flask, request, jsonify, make_response,redirect, url_for,Blueprint
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity,JWTManager,jwt_required
import jwt
from functools import wraps
import uuid
from flask_sqlalchemy import SQLAlchemy
from models import db,User
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
main2=Blueprint("main2", __name__)





jwt=JWTManager(app)

migrate = Migrate(app, db)
ma = Marshmallow(app)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'user_name', 'email', 'password','confirm_password', 'type', 'blocked', 'activity')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return({"message" : "Token is missing"})

        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            
        except:
            return ({"message": "Invalid token"})

        return f(*args, **kwargs)
    return decorated

@main2.route('/superadmin/<token>')
@jwt_required(optional=True)
def superadmin(token):
    return jsonify(token=f"superadmin : {token}")

@main2.route('/admin/<token>')
@jwt_required(optional=True)
def admin(token):
    return jsonify(token=f"admin : {token}")

@main2.route('/customer/<token>')
@jwt_required(optional=True)
def customer(token):
    return jsonify(token=f"student : {token}")

@main2.route('/driver/<token>')
@jwt_required(optional=True)
def driver(token):
    return jsonify(token=f"driver : {token}")

@main2.route('/orders')
@jwt_required(optional=True)
def orders():
    details = get_jwt()
    if details["type"]!='driver':
        return redirect(url_for("guest"))
    return jsonify(detail="info")

@main2.route('/guest')
@jwt_required()
def guest():
    details = get_jwt()
    return jsonify(detail=f"welcome {details['user_name']}")
@main2.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        # Successful login
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


@main2.route('/user', methods=['GET'])
def get_all_users():
     users = User.query.all()

     output = []

     for user in users:
        user_data = {}
        user_data['user_id'] = user.user_id
        user_data['user_name'] = user.user_name
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['confirm_password'] = user.confirm_password
        user_data['type'] = user.type
        user_data['blocked'] = user.blocked
        user_data['activity'] = user.activity
        output.append(user_data)
     return jsonify({'users': output})

 
@main2.route('/user/<user_id>', methods=['GET'])
def get_one_users(user_id):

    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})
    
    user_data = {}
    user_data['user_id'] = user.user_id
    user_data['user_name'] = user.user_name
    user_data['email'] = user.email
    user_data['password'] = user.password
    user_data['confirm_password'] = user.confirm_password
    user_data['type'] = user.type
    user_data['blocked'] = user.blocked
    user_data['activity'] = user.activity
    return jsonify({'users': user_data})
    # pass
 
@main2.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='scrypt')

    new_user = User(user_name=data['user_name'],password=hashed_password, email=data['email'],type=data['type'],blocked=False,activity=False)
    db.session.add(new_user)
    db.session.commit()
    
    return ({'message':'Welcome user'})

@main2.route('/user/<user_id>', methods=['PATCH'])
def user(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})
    
    user.admin = True
    db.session.commit()

    return jsonify({'message': 'User promoted successfully'})

@main2.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User has been deleted'})

# @user.route('/search', methods=['POST','GET'])
# def search():
#     user1 = User.query.filter().all()

    
#     if user1 is None:
#         return jsonify({'message': 'User not found'})
    
#     return jsonify({'message': f'{user=user1.user_name}'})
#     query = request.args.get("query")
#     users = user.query.filter(users.title.like("%"+query+"%")).all()
#     return jsonify({'message': f'{users}'})

    # pass
   
# if __name__ == '_main_':
#     # app.register_blueprint(user)
#     # with app.app_context():
#     #     db.create_all()
#     app.run(debug=True)
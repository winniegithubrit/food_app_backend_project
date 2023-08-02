# # from flask import Flask, jsonify, request, make_response
# # import jwt
# # import datetime
# # from flask_sqlalchemy import SQLAlchemy
# # from model2 import db


# # app = Flask(__name__)
# # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
# # app.config['SECRET_KEY'] = b'\xa6\xf6\x08\x04Z\xfa]\xebT\xaa*X'

# # @app.route('/admin')
# # def admin():
# #     return "Hello admin"

# # @app.route('/customer')
# # def customer():
# #     return "Hello customer"

# # @app.route('/employee')
# # def employee():
# #     return "Hello Employee"

# # @app.route('/login', methods=['POST', 'GET'])
# # def login():
# #     auth = request.authorization

# #     if auth and auth.password == 'password':
# #         token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=59)}, app.config['SECRET_KEY'])

# #         return jsonify({'token': token.decode('UTF-8')})
# #     return make_response('Could not verify!', 401, {'www-Authenticate': 'Basic realm="Login Required"'})

# # if __name__ == '__main__':
# #     app.run(debug=True)
# from flask import Flask, jsonify, request, make_response
# import jwt
# import datetime
# from model2 import db, User

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
# app.config['SECRET_KEY'] = b'\xa6\xf6\x08\x04Z\xfa]\xebT\xaa*X'
# db.init_app(app)

# @app.route('/admin')
# def admin():
#     return "Hello admin"

# @app.route('/customer')
# def customer():
#     return "Hello customer"

# @app.route('/employee')
# def employee():
#     return "Hello Employee"

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     auth = request.authorization

#     if auth and auth.password == 'password':
#         token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=59)}, app.config['SECRET_KEY'])

#         return jsonify({'token': token.decode('UTF-8')})
#     return make_response('Could not verify!', 401, {'www-Authenticate': 'Basic realm="Login Required"'})

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import jwt
import datetime
import uuid
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)

# b'\xa4M/\xdf$v\xa7M\xc4\xaf\xe9\xc2'
app.config['SECRET_KEY'] ='032a7f05a0a64e7cb34dec0646a0b45e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.Boolean, default=False)
    blocked = db.Column(db.Boolean, default=False)
    activity = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password, user_type, blocked, activity):
        self.username = username
        self.email = email
        self.password = password
        self.user_type = user_type
        self.blocked = blocked
        self.activity = activity



class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'username', 'email', 'password', 'user_type', 'blocked', 'activity')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def token_required(f):
     @wraps(f)
     def decorated(*args, **kwargs):
          token = None

          if 'x-access-token' in request.headers:
               token = request.headers['x-access-token']

          if not token:
               return jsonify({'message':'Token missing'}),401
          
          try:
              data = jwt.decode(token,app.config['SECRET_KEY'])
              current_user = User.query.filter_by(user_id=data['user_id']).first()
          except:
               return ({'message': 'Invalid token'}),401
          return f(current_user, *args, **kwargs)
     
     return decorated

@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    
    if not current_user.admin:
         return jsonify({'caanot perform that request'})

    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['user_id'] = user.user_id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['user_type'] = user.user_type
        user_data['blocked'] = user.blocked
        user_data['activity'] = user.activity
        output.append(user_data)
    return jsonify({'users': output})

@app.route('/user/<user_id>', methods=['GET'])
@token_required
def get_one_user(current_user,user_id):
        
        if not current_user.admin:
         return jsonify({'cannot perform that request'})
        
        user = User.query.filter_by(user_id=user_id).first()

        if not user:
             return jsonify({'message': 'No user found'})
        
        user_data = {}
        user_data['user_id'] = user.user_id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['user_type'] = user.user_type
        user_data['blocked'] = user.blocked
        user_data['activity'] = user.activity
        return jsonify({'user': user_data})

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):

    if not current_user.admin:
         return jsonify({'cannot perform that request'})

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password,
                    user_type=False, blocked=False, activity=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Welcome new user'})

@app.route('/user/<user_id>', methods=['PUT'])
@token_required
def update_user(current_user,user_id):
        
        if not current_user.admin:
         return jsonify({'cannot perform that request'})
        
        user = User.query.filter_by(user_id=user_id).first()

        if not user:
             return jsonify({'message': 'No user found'})
        user.admin = True
        db.session.commit()

        return jsonify({'message':'The user has been updated'})

@app.route('/user/<user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
        
        if not current_user.admin:
         return jsonify({'cannot perform that request'})

        user = User.query.filter_by(user_id=user_id).first()

        if not user:
             return jsonify({'message': 'No user found'})
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message':'The user has been deleted'}) 

@app.route('/login')
# @token_required
def login():
     auth = request.authorization()
     if not auth or not auth.username or not auth.password:
          return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required'})
     
     user = User.query.filter_by(username=auth.username).first()

     if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required'})
     
     if check_password_hash(user.password,auth.password):
          token = jwt.encode({'user_id': user.user_id,'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=59)},app.config['SECRET_KEY'])
          return jsonify({'token' : token.decode('UTF-8')})
     
     return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required'})

if __name__ == "__main__":
    app.run(debug=True)

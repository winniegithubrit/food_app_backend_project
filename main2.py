# from flask import Flask, jsonify, request, make_response
# import jwt
# import datetime
# from flask_sqlalchemy import SQLAlchemy
# from model2 import db


# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
# app.config['SECRET_KEY'] = b'\xa6\xf6\x08\x04Z\xfa]\xebT\xaa*X'

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
from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from model2 import db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config['SECRET_KEY'] = b'\xa6\xf6\x08\x04Z\xfa]\xebT\xaa*X'
db.init_app(app)

@app.route('/admin')
def admin():
    return "Hello admin"

@app.route('/customer')
def customer():
    return "Hello customer"

@app.route('/employee')
def employee():
    return "Hello Employee"

@app.route('/login', methods=['POST', 'GET'])
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=59)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify!', 401, {'www-Authenticate': 'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run(debug=True)

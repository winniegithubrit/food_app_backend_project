
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime
from flask_marshmallow import Marshmallow
from models import db
from schemas import *
from flask_jwt_extended import JWTManager
from main2 import main2
from mpesa import mpesa
from Stripe import stripe
from werkzeug.wrappers import Response 



from Restaurant import restaurants
from User import user
from Owner import owners
from Reviews import reviews
# from Stripe import stripe




app = Flask(__name__) 
app.register_blueprint(restaurants)
app.register_blueprint(user)
app.register_blueprint(owners)
app.register_blueprint(reviews)
app.register_blueprint(mpesa)
app.register_blueprint(main2)
app.register_blueprint(stripe)


app.config['SECRET_KEY'] = b'\x06\xf5\xb5\xe6\xf7\x1c\xbd\r\xc5e\xef\xb2\xf1\xcb`\xd8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://steve:gzvhtFOUedOgHo9WaG2R5QCfcsXABXI8@dpg-cj5lg1acn0vc73d98li0-a.oregon-postgres.render.com/dbfoodapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


migrate = Migrate(app, db)
CORS(app,origins='http://localhost:3000')
db.init_app(app)
ma = Marshmallow(app)
jwt=JWTManager(app)


@app.route('/')
def index():
    return {"message": "success"}


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

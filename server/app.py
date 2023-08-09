from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime
from flask_marshmallow import Marshmallow
from models import db
from schemas import *
# from main2 import main2
from mpesa import mpesa




from Restaurant import restaurants
from User import user
from Owner import owners
from Reviews import reviews




app = Flask(__name__)
app.register_blueprint(restaurants)
app.register_blueprint(user)
app.register_blueprint(owners)
app.register_blueprint(reviews)
app.register_blueprint(mpesa)
# app.register_blueprint(main2)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://steve:gzvhtFOUedOgHo9WaG2R5QCfcsXABXI8@dpg-cj5lg1acn0vc73d98li0-a.oregon-postgres.render.com/dbfoodapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


migrate = Migrate(app, db)
CORS(app)
db.init_app(app)
ma = Marshmallow(app)


@app.route('/')
def index():
    return {"message": "success"}


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5955)

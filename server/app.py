from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime
from flask_marshmallow import Marshmallow
from models import db


from Restaurant import restaurants
from User import user
from Owner import owners
from Reviews import reviews



app = Flask(__name__)
app.register_blueprint(restaurants)
app.register_blueprint(user)
app.register_blueprint(owners)
app.register_blueprint(reviews)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://steve:steve@localhost/foodapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


migrate = Migrate(app, db)
CORS(app)
db.init_app(app)
ma = Marshmallow(app)


@app.route('/')
def index():
    return {"message": "success"}


if __name__ == '__main__':
    app.run(port=5855)

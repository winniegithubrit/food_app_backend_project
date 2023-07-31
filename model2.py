# from flask_sqlalchemy import SQLAlchemy
# from main2 import app

# db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(40))
#     secondname = db.Column(db.String(40))
#     email = db.Column(db.String(40), unique=True)
#     password = db.Column(db.String(200))
#     user_type = db.Column(db.String(200), nullable=True)
    
#     def __init__(self, firstname, secondname, email, password, user_type):
#         self.firstname = firstname
#         self.secondname = secondname
#         self.email = email
#         self.password = password
#         self.user_type = user_type
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(200))
    user_type = db.Column(db.String(200), nullable=True)

    def __init__(self, first_name, last_name, email, password, user_type):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.user_type = user_type

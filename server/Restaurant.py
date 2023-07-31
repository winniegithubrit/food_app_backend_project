from flask import Blueprint
restaurants = Blueprint("Restaurant",__name__,)

@restaurants.route('/')
def index():
  return "This is the Products page"

from faker import Faker
from datetime import datetime
from models import db, Owner,Restaurant,Deliveries,Order,Driver,Menu
from app import app
import bcrypt
import random

fake = Faker()



# with app.app_context():
#     db.session.query(Owner).delete()
#     db.session.commit()

#     owners = []
#     for i in range(100):
#         name = fake.name()
#         email = fake.email()
#         password = fake.password() or "defaultpassword"
#         image = fake.image_url(width=None, height=None)

#         # Hash the password
#         hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#         owner = Owner(
#             name=name,
#             email=email,
#             password=hashed_password,
#             image=image
#         )
#         owners.append(owner)

#     db.session.bulk_save_objects(owners)
#     db.session.commit()
# Generate and insert fake data for the Restaurant model

# owner faker data

with app.app_context():
    owners = Owner.query.all()
    db.session.query(Restaurant).delete()
    db.session.commit()
    
    def generate_fake_hours():
      opening_time = fake.time_object().strftime('%H:%M:%S')
      closing_time = fake.time_object().strftime('%H:%M:%S')
      return opening_time, closing_time
    
    restaurants = []
    for _ in range(10): 
        owner = fake.random_element(owners)
        restaurant_name = fake.company()
        contact_number = fake.phone_number()
        opening_hours, closing_hours = generate_fake_hours()
        image = fake.image_url(width=None, height=None)
        payment_method = fake.random_element(['Mpesa', 'Stripe'])

        restaurant = Restaurant(
            owner_id=owner.owner_id,
            restaurant_name=restaurant_name,
            contact_number=contact_number,
            opening_hours=opening_hours,
            closing_hours=closing_hours,
            image=image,
            payment_method=payment_method
        )
        restaurants.append(restaurant)

    db.session.bulk_save_objects(restaurants)
    db.session.commit()
    
with app.app_context():
    orders = Order.query.all()
    drivers = Driver.query.all()

    deliveries = []
    for _ in range(10): 
        order = fake.random_element(orders)
        driver = fake.random_element(drivers)
        delivery_date_and_time = fake.date_time_this_year()

        delivery = Deliveries(
            order_id=order.order_id,
            driver_id=driver.driver_id,
            delivery_date_and_time=delivery_date_and_time,
            dispatch=fake.boolean(),
            delivered=fake.boolean()
        )
        deliveries.append(delivery)

    db.session.bulk_save_objects(deliveries)
    db.session.commit() 

with app.app_context():
    owners = []
    for i in range(20):
        name = fake.name()
        email = fake.email()
        password = fake.password()
        image = fake.image_url(width=None, height=None)

        owner = Owner(
            name=name,
            email=email,
            password=password,
            image=image
        )
        owners.append(owner)

    db.session.bulk_save_objects(owners)
    db.session.commit()

with app.app_context():
    menus = []
    db.session.query(Menu).delete()
    restaurants = Restaurant.query.all()  

    for _ in range(10):
        restaurant = fake.random_element(restaurants)
        menu_name = fake.word().capitalize()
        description = fake.text()
        prices = fake.random_int(min=10, max=100)

        menu = Menu(
            restaurant_id=restaurant.restaurant_id,
            menu_name=menu_name,
            description=description,
            prices=prices
        )
        menus.append(menu)

    db.session.bulk_save_objects(menus)
    db.session.commit()

# with app.app_context():
#     orders = []
#     for _ in range(10):
#         menu_id = fake.random_int(min=1, max=1000)  # Generate random menu IDs between 1 and 1000
#         total_price = fake.random_int(min=10, max=100)
#         order_date_and_time = fake.date_time_this_year()
#         address = fake.address()
#         payment_method = fake.random_element(['Mpesa', 'Stripe'])

#         order = Order(
#             menu_id=menu_id,
#             total_price=total_price,
#             order_date_and_time=order_date_and_time,
#             address=address,
#             payment_method=payment_method
#         )
#         orders.append(order)

#     db.session.bulk_save_objects(orders)
#     db.session.commit()
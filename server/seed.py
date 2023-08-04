from faker import Faker
from datetime import datetime
from models import db, Owner,Restaurant
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
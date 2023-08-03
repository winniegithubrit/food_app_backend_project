from faker import Faker
from datetime import datetime
from models import db, User, Restaurant, Owner
from app import app
import bcrypt
import random

fake = Faker()

with app.app_context():
    # Generate fake users
    db.session.query(User).delete()
    db.session.query(Restaurant).delete()
    db.session.query(Owner).delete()
    db.session.commit()

    users = []
    for i in range(10):
        username = fake.user_name()
        email = fake.email()
        password = fake.password() or "defaultpassword"
        user_type = random.choice([True, False])
        blocked = random.choice([None, 'temporary', 'permanent'])
        activity = fake.text()

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = User(
            user_name=username,
            email=email,
            password=hashed_password,
            type=user_type,
            blocked=blocked,
            activity=activity
        )
        users.append(user)

    db.session.bulk_save_objects(users)
    db.session.commit()

    # Generate fake owners
    owners = []
    for i in range(5):
        owner_name = fake.name()
        owner_email = fake.email()
        owner_password = fake.password() or "defaultpassword"
        owner_image = fake.image_url()

        # Hash the password
        hashed_password = bcrypt.hashpw(owner_password.encode('utf-8'), bcrypt.gensalt())

        owner = Owner(
            name=owner_name,
            email=owner_email,
            password=hashed_password,
            image=owner_image
        )
        owners.append(owner)

    db.session.bulk_save_objects(owners)
    db.session.commit()

    # Generate fake restaurants
    restaurants = []
    for i in range(10):
        owner_id = random.choice(owners).owner_id
        restaurant_name = fake.company()
        contact_number = fake.phone_number()
        opening_hours = datetime.strptime(fake.time(), "%H:%M:%S").time()
        closing_hours = datetime.strptime(fake.time(), "%H:%M:%S").time()
        image = fake.image_url()
        payment_method = random.choice(["Mpesa", "Stripe"])

        restaurant = Restaurant(
            owner_id=owner_id,
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

print("Database seeded successfully.")

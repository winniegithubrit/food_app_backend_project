from faker import Faker
from models import db, Restaurant
from app import app
from datetime import datetime

fake = Faker()

with app.app_context():
    db.session.query(Restaurant).delete()
    db.session.commit()
    
    restaurant_list = []  
    
    for i in range(10):
        restaurant_name = fake.company()
        cuisine_type = fake.random_element(elements=('Italian', 'Chinese', 'Mexican', 'Indian', 'Japanese'))
        contact_number = fake.phone_number()
        
        opening_hours_str = fake.time()  
        opening_hours_time = datetime.strptime(opening_hours_str, '%H:%M:%S').time() 
        
        delivery_fee = fake.random_int(min=0, max=10)  
        image = fake.image_url()
        payment_method = fake.random_element(elements=('Cash', 'Credit Card', 'PayPal', 'Mpesa'))

        restaurant = Restaurant(
            restaurant_name=restaurant_name,
            cuisine_type=cuisine_type,
            contact_number=contact_number,
            opening_hours=opening_hours_time, 
            delivery_fee=delivery_fee,
            image=image,
            payment_method=payment_method
        )
        restaurant_list.append(restaurant) 
    
    db.session.bulk_save_objects(restaurant_list)  
    db.session.commit()

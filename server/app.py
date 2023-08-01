from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime
from flask_marshmallow import Marshmallow
import stripe

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
stripe.api_key = "sk_test_51NaCrLDWZ8VYT067qJD7GMGRRTzNesXgPuOtirmWozS1Ntg6srUUfwu6Mo03Mrm1W5AZOZqTacuzk9LeKrNgvJ9y00re0LPdjZ"

# ... Rest of your code ...

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.get_json()
        amount = data['amount']  # The payment amount in cents

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
        )

        return jsonify(client_secret=intent.client_secret)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(port=5555)

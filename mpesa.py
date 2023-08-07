from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

app = Flask(__name__)

base_url ='http://192.168.0.50:5000'  # Replace this with your actual base URL
consumer_key = '5vMXN1BvxAlxhvt5a67Ah9mD1DQE005r'  # Replace this with your actual consumer key
consumer_secret = 'smY4mdkX1WHucken'  # Replace this with your actual consumer secret

@app.route('/')
def home():
    return 'Hello World!'


def get_access_token():
    endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = r.json()
    return data.get('access_token', None)


@app.route('/access_token')
def access_token():
    token = get_access_token()
    if token:
        return jsonify({'access_token': token})
    else:
        return jsonify({'error': 'Failed to get access token'}), 500


@app.route('/pay', methods=['POST'])
def init_stk():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    access_token = get_access_token()
    if not access_token:
        return jsonify({'error': 'Failed to get access token'}), 500

    headers = {"Authorization": "Bearer %s" % access_token}
    my_endpoint = base_url + "/lnmo"
    Timestamp = datetime.now()
    times = Timestamp.strftime("%Y%m%d%H%M%S")
    password = "your_shortcode_here" + "your_passkey_here" + times
    datapass = base64.b64encode(password.encode('utf-8'))

    data = {
    "BusinessShortCode": 174379,
    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMwODA3MTA1MjQ2",
    "Timestamp": "20230807105246",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": 254759212840,
    "PartyB": 174379,
    "PhoneNumber": 254759212840,
    "CallBackURL": "https://mydomain.com/path",
    "AccountReference": "MunchHub",
    "TransactionDesc": "Payment of X" 
  }
    res = requests.post(endpoint, json=data, headers=headers)
    return jsonify(res.json())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

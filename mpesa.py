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


@app.route('/register', methods=['POST'])
def register_urls():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
    access_token = get_access_token()
    if not access_token:
        return jsonify({'error': 'Failed to get access token'}), 500

    my_endpoint = base_url + "c2b/"
    headers = {"Authorization": "Bearer %s" % access_token}
    r_data = {
        "ShortCode": "600383",
        "ResponseType": "Completed",
        "ConfirmationURL": my_endpoint + 'con',
        "ValidationURL": my_endpoint + 'val'
    }

    response = requests.post(endpoint, json=r_data, headers=headers)
    return jsonify(response.json())


@app.route('/simulate', methods=['POST'])
def simulate_payment():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
    access_token = get_access_token()
    if not access_token:
        return jsonify({'error': 'Failed to get access token'}), 500

    headers = {"Authorization": "Bearer %s" % access_token}

    data_s = {
        "Amount": 100,
        "ShortCode": "600383",
        "BillRefNumber": "test",
        "CommandID": "CustomerPayBillOnline",
        "Msisdn": "254759212840"
    }

    res = requests.post(endpoint, json=data_s, headers=headers)
    return jsonify(res.json())


@app.route('/b2c', methods=['POST'])
def b2c_payment():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'
    access_token = get_access_token()
    if not access_token:
        return jsonify({'error': 'Failed to get access token'}), 500

    headers = {"Authorization": "Bearer %s" % access_token}
    my_endpoint = base_url + "/b2c/"

    data = {
        "InitiatorName": "apitest342",
        "SecurityCredential": "your_security_credential_here",
        "CommandID": "BusinessPayment",
        "Amount": "200",
        "PartyA": "601342",
        "PartyB": "254759212840",
        "Remarks": "Pay Salary",
        "QueueTimeOutURL": my_endpoint + "timeout",
        "ResultURL": my_endpoint + "result",
        "Occasion": "Salary"
    }

    res = requests.post(endpoint, json=data, headers=headers)
    return jsonify(res.json())


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
    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMwODA2MTIzODM4",
    "Timestamp": "20230806123838",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": 254759212840,
    "PartyB": 174379,
    "PhoneNumber": 254759212840,
    "CallBackURL": "https://mydomain.com/path",
    "AccountReference": "CompanyXLTD",
    "TransactionDesc": "Payment of X" 
  }

    res = requests.post(endpoint, json=data, headers=headers)
    return jsonify(res.json())


@app.route('/lnmo-callback', methods=['POST'])
def lnmo_result():
    data = request.get_data()
    with open('lnmo.json', 'a') as f:
        f.write(data)
    return jsonify({'message': 'Callback received'})


@app.route('/b2c/result', methods=['POST'])
def result_b2c():
    data = request.get_data()
    with open('b2c.json', 'a') as f:
        f.write(data)
    return jsonify({'message': 'Callback received'})


@app.route('/b2c/timeout', methods=['POST'])
def b2c_timeout():
    data = request.get_json()
    with open('b2ctimeout.json', 'a') as f:
        f.write(data)
    return jsonify({'message': 'Callback received'})


@app.route('/c2b/val', methods=['POST'])
def validate():
    data = request.get_data()
    with open('data_v.json', 'a') as f:
        f.write(data)
    return jsonify({'message': 'Validation received'})


@app.route('/c2b/con', methods=['POST'])
def confirm():
    data = request.get_json()
    with open('data_c.json', 'a') as f:
        f.write(json.dumps(data))
    return jsonify({'message': 'Confirmation received'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

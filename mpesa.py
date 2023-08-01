# from flask import Flask,request
# import requests
# from requests.auth import HTTPBasicAuth
# import json

# app = Flask(__name__)

# consumer_key = '5vMXN1BvxAlxhvt5a67Ah9mD1DQE005r'
# consumer_secret = 'smY4mdkX1WHucken'
# base_url = ''

# #access_token
# @app.route('/access_token')
# def token():
#       data = ac_token()
#       return data

 

# @app.route('/register_urls')
# def register():
#       mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
#       headers = {"Authorization": "Bearer %s" }
#       req_body={
#             "Shortcode": "601426", 
#             "ResponseType": "completed",
#             "ConfirmationURL": base_url + "/c2b/confirm",
#             "ValidationURL": base_url + "/c2b/validation"  
#             },
#       response_data = requests.post(
#             mpesa_endpoint,
#             json = req_body,
#             headers = headers
#             )

#       return response_data.json()

# @app.route('/c2b/confirm')
# def confirm():
#       data = request.get_json()
#       file = open('confirm.json','a')
#       file.write(json.dumps(data))
#       file.close()
#       return{
#            "ResultCode": 0,
#            "ThridPartyTransID":"Yay_my_server",
#            "ResultDesc": "Accepted"

#       }

# @app.route('/c2b/validation')
# def validation():
#       data = request.get_json()
#       file = open('validate.json','a')
#       file.write(json.dumps(data)) 
#       file.close()
#       return{
#            "ResultCode": 0,
#            "ResultDesc": "Accepted"
#       }

# @app.route('/simulate')
# def simulate(): 
#       mpesa_endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
#       access_token = ac_token

#       headers = {"Authorization": "Bearer %s" % access_token}
#       request_body = {
#             "ShortCode":"601426",
#             "CommandID":"CustomerPayBillOnline",
#             "BillRefNumber":"TestPay",
#             "Msisdn":"254759212840",
#             "Amount":50
#       }

#       simulate_response = requests.post(mpesa_endpoint,json = request_body, headers = headers)

#       return simulate_response.json()

# def ac_token():
#     mpesa_auth_url='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
#     data = requests.get(mpesa_auth_url, auth = HTTPBasicAuth(consumer_key, consumer_secret)).json()
#     return data['access_token']

# if __name__ == "__main__":
# 	app.run(debug=True)
from flask import Flask, request
import requests
from requests.auth import HTTPBasicAuth
import json

app = Flask(__name__)

consumer_key = '5vMXN1BvxAlxhvt5a67Ah9mD1DQE005r'
consumer_secret = 'smY4mdkX1WHucken'
base_url = ''

# access_token
@app.route('/access_token')
def token():
    data = ac_token()
    return data

@app.route('/register_urls')
def register():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    access_token = ac_token()

    headers = {"Authorization": "Bearer %s" % access_token}
    req_body = {
        "Shortcode": "174379", 
        "ResponseType": "completed",
        "ConfirmationURL": base_url + "/c2b/confirm",
        "ValidationURL": base_url + "/c2b/validation"
    }
    response_data = requests.post(
        mpesa_endpoint,
        json=req_body,
        headers=headers
    )

    return response_data.json()

@app.route('/c2b/confirm', methods=['POST'])
def confirm():
    data = request.get_json()
    with open('confirm.json', 'a') as file:
        file.write(json.dumps(data))
    return {
        "ResultCode": 0,
        "ThridPartyTransID": "Yay_my_server",
        "ResultDesc": "Accepted"
    }

@app.route('/c2b/validation', methods=['POST'])
def validation():
    data = request.get_json()
    with open('validate.json', 'a') as file:
        file.write(json.dumps(data))
    return {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

@app.route('/simulate')
def simulate():
    mpesa_endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    access_token = ac_token()

    headers = {"Authorization": "Bearer %s" % access_token}
    request_body = {
        "ShortCode": "174379",
        "CommandID": "CustomerPayBillOnline",
        "BillRefNumber": "TestPay",
        "Msisdn": "254759212840",
        "Amount": 50
    }

    simulate_response = requests.post(mpesa_endpoint, json=request_body, headers=headers)

    return simulate_response.json()

def ac_token():
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    data = requests.get(mpesa_auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret)).json()
    return data['access_token']

if __name__ == "__main__":
    app.run(debug=True)

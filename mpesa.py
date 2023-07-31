from flask import Flask
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

consumer_key = '5vMXN1BvxAlxhvt5a67Ah9mD1DQE005r'
consumer_secret = 'smY4mdkX1WHucken'

@app.route('/access_token')
def token():
    mpesa_auth_url='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    data = requests.get(mpesa_auth_url, auth = HTTPBasicAuth(consumer_key, consumer_secret)).json()
    return data

@app.route('/home')
def home():
    return 'Hello World'

# if __name__ == 'main':
#      app.run(debug=True)
if __name__ == "__main__":
	app.run(debug=True)
# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# if __name__ == "__main__":
# 	app.run(debug=True)
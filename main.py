from smartly import Smartly
import requests
from flask import Flask, request
app = Flask(__name__)


chatbot = Smartly(platform="messenger", name = "Smartly",
                  token='EAALa1uQGPg8BAIwAyFNAWSMzslR8Vu2qnkHmZBNOkYojzAsfb9ZBlmclE8SHvRCD5dSeijBGYZCxpfhuglL'
                        'aZCbusczNiZAS9QMoh7MbeJRveYDrZBZATTuTh6tCL3xjLZA1'
                        'Us7LhR5jZCKF0vwIStJr3ZAfFnm6rd0lXZBYL8Mk38q5ahFaar2aZC0M')

@app.route('/')
def hello_world():
    return 'Hello, World!'


# Adds support for GET requests to our webhook
@app.route('/webhook', methods=['GET'])
def webhook_authorization():
    verify_token = request.args.get("hub.verify_token")
    # Check if sent token is correct
    if verify_token == "amazingct":
        # Responds with the challenge token from the request
        return request.args.get("hub.challenge")
    return 'Unable to authorize.'


@app.route("/webhook", methods=['POST'])
def webhook_handle():
    data = request.get_json()
    response = chatbot.reply(data)
    if response is not None:
        return response
    return 'ok'


if __name__ == "__main__":
    app.run(threaded=True, port=5000)

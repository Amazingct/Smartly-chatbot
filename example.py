from smartly import Smartly, Text, Button, Image, Card
from flask import Flask, request
app = Flask(__name__)
image_url = "https://scontent.flos5-1.fna.fbcdn.net/v/t1.0-9/120101610_102735164929182_997212438658305435_o.jpg?_nc_cat=109&ccb=2&_nc_sid=e3f864&_nc_eui2=AeGnZk5OnOgfCyg6ZZk_yl-oP_W4FNqvccc_9bgU2q9xx6Ro-9cCQE-KNL8k1qP0bE6yA6-b1d2g5LJNXpZW9JgW&_nc_ohc=EqdCyRNeQlQAX8ESh3c&_nc_ht=scontent.flos5-1.fna&oh=fdf28ee2087e05912fd74bed382ef910&oe=600C3CF7"


class Chatbot(Smartly):
    def __init__(self, name, platform, token):
        super().__init__(platform = platform, name= name, token = token)

    def generate_response(self, message):
        if message == "text":
            response = Text("Hello, my name is {}, I am Mr Dan's personal AI assistance, how may i help you today?".format(self.name)).message()

        elif message == "image":
            response = Image(image_url).message()

        elif message == "button":
            b = Button(title = "Choose a color")
            b.add( content_type ="text", title = "Red", payload = "")
            b.add( content_type ="text", title = "blue", payload = "")
            b.add(content_type="text", title="yellow", payload="")
            response = b.message()

        elif message == "card":
            c = Card(title="Chat with Agent", url = "google.com")
            c.image(image_url)
            c.add_button(type="web_url", url="google.com", title="FEMI")
            c.add_button(type="web_url", url ="google.com", title = "BUKKY")
            c.add_button(type="web_url", url="google.com", title="DANIEL")
            # c.add_button(type="postback",title="Start Chatting", payload="DEVELOPER_DEFINED_PAYLOAD")
            c.subtitle = "yeeeee"
            response = c.message()

        return response


chatbot = Chatbot(platform="messenger", name = "Smartly",
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

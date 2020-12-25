import requests
from requests_toolbelt import MultipartEncoder
image_url = "https://scontent.flos5-1.fna.fbcdn.net/v/t1.0-9/120101610_102735164929182_997212438658305435_o.jpg?_nc_cat=109&ccb=2&_nc_sid=e3f864&_nc_eui2=AeGnZk5OnOgfCyg6ZZk_yl-oP_W4FNqvccc_9bgU2q9xx6Ro-9cCQE-KNL8k1qP0bE6yA6-b1d2g5LJNXpZW9JgW&_nc_ohc=EqdCyRNeQlQAX8ESh3c&_nc_ht=scontent.flos5-1.fna&oh=fdf28ee2087e05912fd74bed382ef910&oe=600C3CF7"


def package_message(data, type="String", source="text"):
    if source == "url" and type == "image":
        message = {"attachment": {"type": "image", "payload": {
                                    'url': data}}}

    elif source == "text" and type == "String":
        message = {'text':data}

    elif source == "file":
        pass
    return message


class Smartly:
    def __init__(self, name="chatbot", platform="messenger", **config):
        self.name = name
        self.type = config
        self.platform = platform
        self.config = config

    def generate_response(self, message):
        # do any AI stuff  here
        response = package_message("Hello, my name is {}, I am Mr Dan's personal AI assistance, how may i help you today?".format(self.name), type ="String")
        # response = package_message(image_url, type="image", source="url")
        return response

    def reply(self, data):
        ##### message from messenger ######
        if self.platform == "messenger":
            try:
                message = data['entry'][0]['messaging'][0]['message']["text"]
                print("received >> ", message)
                sender_id = data['entry'][0]['messaging'][0]['sender']['id']
                reply = self.generate_response(message)
                request_body = {'recipient': {'id': sender_id},'message':reply }
                response = requests.post('https://graph.facebook.com/v9.0/me/messages?access_token=' + self.config['token'], json=request_body).json()
                print("sent >> ", reply)
                return response
            except Exception as e:
                print(e)
                return None

        elif self.platform == "telegram":
            pass
        else:
            pass






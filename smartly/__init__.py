import requests
sender_id = None


class Image:
    def __init__(self, link):
        self.url = link

    def message(self):
        return {"attachment": {"type": "image", "payload": {'url': self.url}}}


class Card:
    def __init__(self, title, url):
        self.buttons = []
        self.title = title
        self.subtitle = ""
        self.url = url


    def add_button(self, **config):
       self.buttons.append(config)

    def image(self, image_url):
        self.image_url = image_url
        pass

    def message(self):
        return {

    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
           {
            "title":self.title,
            "image_url":self.image_url,
            "subtitle":self.subtitle,
            "default_action": {
              "type": "web_url",
              "url": self.url,
              "webview_height_ratio": "tall",
            },
            "buttons":self.buttons
          }
        ]
      }}}


class Text:
    def __init__(self, text):
        self.text = text

    def message(self):
        return  {'text':self.text}


class Button:
    def __init__(self, title):
        self.buttons = []
        self.title = title

    def add(self, **config):
        self. buttons.append(config)

    def message(self):
        return {"text": self.title, "quick_replies": self.buttons}


class Flow:
    def __init__(self, name, **config):
        pass


class Smartly:
    def __init__(self, name="chatbot", platform="messenger", **config):
        self.name = name
        self.type = config
        self.platform = platform
        self.config = config

    def get_sender_info(self):
        info = requests.get(
            "https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}".format(sender_id,
                                                                                                self.config['token'])).json()
        return info

    def generate_response(self, message, sender=None):
        # do any AI stuff  here
        print("generating reply...")

    def reply(self, data):
        global sender_id
        ##### message from messenger ######
        if self.platform == "messenger":
            try:
                message = data['entry'][0]['messaging'][0]['message']["text"].lower()
                print("received >> ", message)
                sender_id = data['entry'][0]['messaging'][0]['sender']['id']
                reply = self.generate_response(message, sender_id)
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


class Database:
    pass




import requests
from requests.exceptions import *


class Client(object):
    def __init__(self):
        self.server = 'http://localhost:5000/api'
        pass

    def register(self, user, email, password):
        try:
            r = requests.post(self.server, data={
                    "username": user,
                    "email": email,
                    "password": password
                })
            print(r.text)

        except ConnectionRefusedError as e:
            print("Connection refused")

        except ConnectionError as e:
            print("Connection error:", e)

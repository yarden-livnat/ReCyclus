import json
from pathlib import Path
import requests
from requests_jwt import JWTAuth
from requests.exceptions import *
from requests.auth import AuthBase


class JWTAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r


class Client(object):
    def __init__(self):
        self.server = 'http://localhost:5000/api'
        self.tokens = {'access_token': None, 'refresh_token': None}
        self._load()

    def _save(self):
        with open('auth.json', 'w') as f:
            json.dump(self.tokens, f)

    def _load(self):
        if Path('auth.json').exists():
            with open('auth.json') as f:
                self.tokens = json.load(f)
            self.auth = JWTAuth(self.tokens['access_token'])

    def register(self, user, password):
        try:
            reply = requests.post(self.server+'/admin/register',
                              data={
                                    "username": user,
                                    "password": password
                                })
            print("content:", reply.content)
            r = json.loads(reply.content)
            if reply.status_code == 201:
                self.tokens= r['Authorization']
                self._save()
                self._load()
                print('ok')
            else:
                raise ValueError(r['message'])

        except ConnectionRefusedError as e:
            print("Connection refused")
            raise ConnectionError(e)

        except ConnectionError as e:
            print("Connection error:", e)
            raise ConnectionError(e)

    def test(self):
        r = requests.get(self.server + '/auth/token', auth=self.auth)
        return r

    def run(self, sim=None, name=None):
        payload = {
        }
        if name is not None:
            payload['name'] = name
        if sim is not None:
            payload['sim'] = sim

        r = requests.post(self.server+'/services/batch/run', data=payload, auth=self.auth)

        return r

    # def fetch(self, filename, jobid, name=None):
    #     payload = {
    #         'jobid': jobid,
    #         'filename': filename,
    #     }
    #     if name is not None:
    #         payload['name'] = name
    #     r = requests.get(self.server + '/services/datastore/fetch', data=payload, stream=False, auth=JWTAuth(self.auth['access_token']))
    #     return r

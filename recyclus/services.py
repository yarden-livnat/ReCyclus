import requests
import yaml
from pathlib import Path

from .config import config
from .auth import Auth
from requests.exceptions import *

auth = Auth()


def protect(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ConnectionRefusedError as e:
            print("Connection refused")
            raise ConnectionError(e)

        except ConnectionError as e:
            print("Connection error:", e)
            raise ConnectionError(e)
    return wrapper


class Services(object):
    def __init__(self, config_file=None):
        self.config = config
        self.auth = auth
        self.load_config(config_file)
        self.auth.load(self.config['auth_file'])
        self.server = self.config['server']

    def load_config(self, config_file=None):
        config_file = config_file or self.config['config_file']
        config_file = Path(config_file)
        if config_file.exists():
            with open(config_file, 'r') as f:
                cfg = yaml.load(f, Loader=yaml.FullLoader)
                self.config = {**self.config, **cfg}

    def save_config(self):
        with open(self.config['config_file'], 'w') as f:
            yaml.dump(self.config, f)

    def credentials(self, user, token):
        self.config['user'] = user
        self.save_config()
        self.auth.token = token
        self.auth.save(self.config['auth_file'])

    def url(self, service, server):
        return f'{server or self.server}/{service}'

    @protect
    @auth.authenticate
    def get(self, service, server=None, *args, **kwargs):
        r = requests.get(self.url(service, server), *args, **kwargs)
        r.raise_for_status()
        return r

    @protect
    @auth.authenticate
    def post(self, service, server=None, *args, **kwargs):
        r = requests.post(self.url(service, server), *args, **kwargs)
        r.raise_for_status()
        return r

    @protect
    @auth.authenticate
    def put(self, service, server=None, *args, **kwargs):
        r = requests.put(self.url(service, server), *args, **kwargs)
        r.raise_for_status()
        return r

    @protect
    @auth.authenticate
    def delete(self, service, server=None, **kwargs):
        r = requests.delete(self.url(service, server), **kwargs)
        r.raise_for_status()
        return r

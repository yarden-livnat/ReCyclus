from pathlib import Path
from requests.auth import AuthBase


class Auth(AuthBase):
    def __init__(self):
        self.token = ''

    def load(self, path):
        if path.exists():
            with open(path, 'r') as f:
                self.token = f.readline()
            path.chmod(0o600)

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(self.token)
        path.chmod(0o600)

    def authenticate(self, f):
        def wrapper(*args, auth=self, **kwargs):
            return f(*args, **kwargs, auth=auth)
        return wrapper

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r


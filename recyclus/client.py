import json
import getpass
from pathlib import Path
from pprintpp import pprint
from requests_toolbelt import MultipartEncoder

from .services import Services


class Client(Services):
    def __init__(self):
        super().__init__()

    def register(self, user=None, password=None):
        if user is None:
            user = getpass.getuser()
        if password is None:
            password = getpass.getpass()

        reply = self.post('admin/register',
                          data={"username": user, "password": password})
        r = json.loads(reply.content)
        if reply.status_code == 201:
            self.credentials(user=user, token=r['token'])
            print('ok')
        else:
            raise ValueError(r.get('message', 'unexpected return code'))

    def login(self, user=None, password=None):
        if user is None:
            user = getpass.getuser()
        if password is None:
            password = getpass.getpass()

        reply = self.post('auth/login',
                          data={"username": user, "password": password})
        r = json.loads(reply.content)
        if reply.status_code == 200:
            self.credentials(user=user, token=r['token'])
            print('logged in')
        else:
            raise ValueError(r.get('message', 'unexpected return code'))

    def test(self):
        r = self.get('auth/token', auth=self.auth)
        return r

    #
    # batch services
    #

    def run(self, scenario, format='sqlite', name=None):
        data = {}
        if name is not None:
            data['name'] = name

        sim = dict(format=format)
        files = None
        if type(scenario) == str:
            filename = Path(scenario)
            if not filename.exists():
                raise FileNotFoundError
            with open(scenario, 'r') as f:
                sim['scenario'] = f.read()
                sim['scenario_filename'] = filename.name
        else:
            sim['scenario'] = scenario

        data['simulation'] = sim
        r = self.post('batch/run', json=data)
        return r.json()

    def status(self, jobid):
        return self.get(f'batch/status/{jobid}').json()

    #
    # datastore services
    #

    def files(self, name=None, jobid=None, pp=False):
        payload = {}
        if name is not None:
            payload['name'] = name
        if jobid is not None:
            payload['jobid'] = jobid

        r = self.get('datastore/files', json=payload).json()
        if pp:
            pprint(r)
        return r

    def fetch(self, filename, jobid, name=None):
        payload = {
            'jobid': jobid,
            'filename': filename,
        }
        if name is not None:
            payload['name'] = name
        r = self.get('datastore/fetch', json=payload, stream=False)
        return r.content

    def save(self, filename, jobid, to=None, name=None):
        if to is None:
            to = filename
        raw = self.fetch(filename, jobid, name)
        with open(to, 'wb') as f:
            f.write(raw)

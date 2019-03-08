import json
import getpass
from pathlib import Path
from pprintpp import pprint

from .services import Services
from .job import Job


class Client(object):
    def __init__(self):
        self.services = Services()

    def server(self, url=None):
        if url is None:
            return self.services.server
        self.services.server = url

    #
    # admin services
    #

    def register(self, user=None, password=None):
        if user is None:
            user = getpass.getuser()
        if password is None:
            password = getpass.getpass()

        reply = self.services.post('admin/register',
                          data={"username": user, "password": password})
        r = json.loads(reply.content)
        if reply.status_code == 201:
            self.services.credentials(user=user, token=r['token'])
            print('ok')
        else:
            raise ValueError(r.get('message', 'unexpected return code'))

    def login(self, user=None, password=None):
        if user is None:
            user = getpass.getuser()
        if password is None:
            password = getpass.getpass()

        reply = self.services.post('auth/login',
                          data={"username": user, "password": password})
        r = json.loads(reply.content)
        if reply.status_code == 200:
            self.services.credentials(user=user, token=r['token'])
            print('logged in')
        else:
            raise ValueError(r.get('message', 'unexpected return code'))

    def test(self):
        r = self.services.get('auth/token', auth=self.services.auth)
        return r

    def job(self, jobid, name):
        return Job(self, jobid=jobid, name=name)

    #
    # batch services
    #

    def run(self, scenario, format='sqlite', name=None, post=None):
        job = Job(self, scenario, format, name, post)
        return job.run()

    def status(self, jobid):
        return self.services.get(f'batch/status/{jobid}').json()

    def cancel(self, jobid):
        return self.services.delete(f'batch/cancel/{jobid}').json()

    def delete(self, jobid):
        return self.services.delete(f'batch/delete/{jobid}')

    #
    # datastore services
    #

    def files(self, name=None, jobid=None, pp=False):
        payload = {}
        if name is not None:
            payload['name'] = name
        if jobid is not None:
            payload['jobid'] = jobid

        r = self.services.get('datastore/files', json=payload).json()
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
        r = self.services.get('datastore/fetch', json=payload, stream=False)
        return r.content

    def save(self, filename, jobid, to=None, name=None):
        if to is None:
            to = filename
        raw = self.services.fetch(filename, jobid, name)
        with open(to, 'wb') as f:
            f.write(raw)


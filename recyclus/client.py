import getpass
import json
from requests.exceptions import HTTPError

from .services import Services
from .job import Job


class Client(object):
    def __init__(self):
        self.services = Services()

    def server(self, host=None):
        if host is None:
            return self.services.server
        self.services.server = f'http://{host}:5000/api'

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

    def job(self, jobid, project=None):
        return Job(self, jobid=jobid, project=project)

    #
    # batch services
    #

    def run(self, scenario, format='sqlite', project=None, post=None):
        job = Job(self, scenario, format, project, post)
        return job.run()

    def status(self, jobid):
        return self.services.get(f'batch/status/{jobid}').json()

    def cancel(self, jobid):
        return self.services.delete(f'batch/cancel/{jobid}').json()

    def delete(self, jobid):
        return self.services.delete(f'batch/delete/{jobid}').json()

    #
    # datastore services
    #

    def files(self, project=None, jobid=None):
        payload = {}
        if project is not None:
            payload['project'] = project
        if jobid is not None:
            payload['jobid'] = jobid

        r = self.services.get('datastore/files', json=payload).json()
        return r

    def list(self, project=None, jobid=None):
        files = self.files(project, jobid)
        user = None
        project = None
        for entry in files:
            if entry['user'] != user:
                user = entry['user']
                print('User:', user)
                project = None
            if entry['project'] != project:
                project  = entry['project']
                print('\tProject:', project)
            print(f"\t\tJob: {entry['jobid']}    Files: {entry['files']}")

    def fetch(self, filename, jobid, project=None):
        payload = {
            'jobid': jobid,
            'filename': filename,
        }
        if project is not None:
            payload['project'] = project
        r = self.services.get('datastore/fetch', json=payload, stream=False)
        return r.content

    def save(self, filename, jobid, to=None, project=None):
        if to is None:
            to = filename
        try:
            raw = self.fetch(filename, jobid, project)
            with open(to, 'wb') as f:
                f.write(raw)
        except HTTPError:
            print('Error: file not found')


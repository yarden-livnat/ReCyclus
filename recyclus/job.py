from pathlib import Path


class Job(object):
    def __init__(self, client, scenario=None, format='sqlite', name='default', post=None, jobid=None):
        self.client = client
        self.scenario = scenario
        self.format = format
        self.name = name
        self.post = post
        self.jobid = jobid

    def run(self):
        payload = {}
        if self.name is not None:
            payload['name'] = self.name

        payload['tasks'] = tasks = {}
        tasks['simulation'] = sim = dict(format=self.format)
        files = None
        if type(self.scenario) == str:
            filename = Path(self.scenario)
            with open(self.scenario, 'r') as f:
                sim['scenario'] = f.read()
                sim['scenario_filename'] = filename.name
        elif type(self.scenario) == dict:
            sim['scenario'] = self.scenario
        else:
            raise ValueError('scenario must be a filename or a dictionary')

        if self.post is not None:
            if type(self.post) == str:
                tasks['post'] = post = {}
                filename = Path(self.post)
                with open(filename, 'r') as f:
                    post['script'] = f.read()
                    post['script_filename'] = filename.name
            elif type(self.post) == dict:
                tasks['script'] = self.post
            else:
                raise ValueError('post must be a filename or a dictionary')

        r = self.client.post('batch/run', json=payload)
        r.raise_for_status()
        info = r.json()
        if 'jobid' in info:
            self.jobid = info['jobid']
        else:
            raise Exception(f'unexpected reply from server: {r.text}')

        return self

    def status(self):
        r = self.client.status(jobid=self.jobid)
        return r

    def cancel(self):
        return self.client.cancel(self.jobid)

    def files(self):
        r = self.client.files(name=self.name, jobid=self.jobid)
        if len(r) > 0:
            return r[0]['files']
        return 'no files found'

    def fetch(self, filename):
        return self.client.fetch(filename, jobod=self.jobid, name=self.name)

    def save(self, filename):
        return self.client.save(filename, jobid=self.jobid, name=self.name)

    def delete(self):
        return self.client.delete(jobid=self.jobid)

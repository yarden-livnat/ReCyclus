from pathlib import Path


class Job(object):
    def __init__(self, client, scenario=None, format='sqlite', project='default', post=None, jobid=None):
        self.client = client
        self.scenario = scenario
        self.format = format
        self.project = project
        self.post = post
        self.jobid = jobid

    def run(self):
        payload = {}
        if self.project is not None:
            payload['project'] = self.project

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

        r = self.client.services.post('batch/run', json=payload)
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
        r = self.client.files(project=self.project, jobid=self.jobid)
        if len(r) > 0:
            return r[0]['files']
        return 'no files found'

    def fetch(self, filename):
        return self.client.fetch(filename, jobod=self.jobid, project=self.project)

    def save(self, filename, to=None):
        return self.client.save(filename, jobid=self.jobid, project=self.project, to=to)

    def delete(self):
        return self.client.delete(jobid=self.jobid)

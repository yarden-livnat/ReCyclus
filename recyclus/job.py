from pathlib import Path


class Job(object):
    def __init__(self, client, scenario=None, format='sqlite', name='default', jobid=None):
        self.client = client
        self.scenario = scenario
        self.format = format
        self.name = name
        self.jobid = jobid

    def run(self):
        data = {}
        if self.name is not None:
            data['name'] = self.name

        sim = dict(format=self.format)
        files = None
        if type(self.scenario) == str:
            filename = Path(self.scenario)
            if not filename.exists():
                raise FileNotFoundError
            with open(self.scenario, 'r') as f:
                sim['scenario'] = f.read()
                sim['scenario_filename'] = filename.name
        else:
            sim['scenario'] = self.scenario

        data['simulation'] = sim
        r = self.client.post('batch/run', json=data).json()
        self.jobid = r['jobid']
        return self

    def status(self):
        r = self.client.status(jobid=self.jobid)
        return r['status']

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

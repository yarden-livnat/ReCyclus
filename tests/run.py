import pp
from recyclus import Client
import time


def load(job):
    print('fetching cyclus.sqlite...')
    client.save('cyclus.sqlite', job.jobid)


client = Client()

job = client.run(scenario='./scenario.xml', project='a')

print('job submitted:', job.jobid)

while True:
    time.sleep(2)
    # print('\tchecking status...')
    resp = job.status()
    if resp['status'] != 'ok':
        print(f'Error:', resp['message'])
        break

    info = resp['info']
    print(f"\tStatus: {info['status']} {info.get('error', '')}")

    if info['status'] in ['done', 'error', 'unknown job']:
        if info['status'] == 'done':
            load(job)
            # job.delete()
            print('done')
        break




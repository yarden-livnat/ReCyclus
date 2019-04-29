from recyclus import Client
import time


def load(job):
    print('fetching cyclus.sqlite...')
    client.save('cyclus.sqlite', job.jobid)


def wait_for_completion(job):
    while True:
        time.sleep(2)
        resp = job.status()
        if resp['status'] != 'ok':
            print(f'Error:', resp['message'])
            return

        info = resp['info']
        print(f"\tStatus: {info['status']} {info.get('error', '')}")

        if info['status'] in ['done', 'error', 'unknown job']:
            if info['status'] == 'done':
                load(job)
                # job.delete()
                print('done')
            return


client = Client()
job = client.run(scenario='./scenario.xml', project='demo')

wait_for_completion(job)
print('job submitted:', job.jobid)


print('files:',job.files)

print('list:')
job.list()




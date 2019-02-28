import pp
from recyclus import Client
import time

client = Client()

# r = client.run(sim={
#     'scenario': 'very_bad_scenario'
# })

# with open('./scenario.xml', 'r') as f:
#     scenario = f.read()

r = client.run(scenario='./scenario.xml')

jobid = r['jobid']
print('jobid:', jobid)

while True:
    print('wait...')
    time.sleep(2)
    r = client.status(jobid)
    if r['status'] in ['done', 'error', 'unknown job']:
        print(f"{r['status']} {r.get('error', '')}")
        break
if r['status'] == 'done':
    print('fetching file...')
    # r = client.fetch('cyclus.sqlite', jobid)
    client.save('cyclus.sqlite', jobid,)

import pp
from recyclus import Client
import time

client = Client()

job = client.run(scenario='./scenario.xml')

print('jobid:', job.jobid)

# while True:
#     print('wait...')
#     time.sleep(2)
#     job.status()
#     if r['status'] in ['done', 'error', 'unknown job']:
#         print(f"{r['status']} {r.get('error', '')}")
#         break
# if r['status'] == 'done':
#     print('fetching file...')
#     # r = client.fetch('cyclus.sqlite', jobid)
#     client.save('cyclus.sqlite', jobid,)

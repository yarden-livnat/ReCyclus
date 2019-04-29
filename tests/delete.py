from recyclus import Client

client = Client()
job = client.job('yarden:default-4', 'test')
print(job.files())

r = job.delete()
print(r)

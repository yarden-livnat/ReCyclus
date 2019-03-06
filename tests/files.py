from recyclus import Client

client = Client()
job = client.job('yarden:bad-1', 'bad')
print(job.files())

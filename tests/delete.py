from recyclus import Client

client = Client()
job = client.job('yarden:demo-3')
print(job.files())

job.delete()


from recyclus import Client

client = Client()
# job = client.job('yarden:default-2', 'test')
# print(job.files())
print(client.files())

print('**list')
client.list()
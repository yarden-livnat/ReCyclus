
from recyclus import Client

client = Client()

r = client.files(name='default',pp=True)

print(r)

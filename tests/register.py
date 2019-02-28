from recyclus import Client

client = Client()

user = 'user5'
client.register(password='password')
print('registered user:', user)

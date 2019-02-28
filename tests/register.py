from recyclus import Client

client = Client()

user = 'user1'
client.register(user, 'password')
print('registered user:', user)

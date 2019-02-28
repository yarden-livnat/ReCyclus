

from recyclus import Client

client = Client()

r = client.run(sim={
    'scenario': 'very_bad_scenario'
})

print(r.content)

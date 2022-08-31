import requests

url = 'http://localhost:5000/users'

x = requests.get(url)
print(x.text)

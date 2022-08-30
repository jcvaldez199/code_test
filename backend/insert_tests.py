import requests

url = 'http://localhost:5000/users'

# test normal 3 inserts
ins1 = {'name':'Alamone','mail':'lol@lol.lol', 'mode':'add'}
x = requests.post(url,json=ins1)
print(x.text)

ins2 = {'name':'Bastian','mail':'yahoo@gmail.lol', 'mode':'add'}
x = requests.post(url,json=ins2)
print(x.text)

ins3 = {'name':'Crikey','mail':'wew@lad.xd', 'mode':'add'}
x = requests.post(url,json=ins3)
print(x.text)

# get all the new users
x = requests.get(url)
print(x.text)

# delete one user
ins = {'userid':1, 'mode':'del'}
x = requests.post(url,json=ins)
print(x.text)

# delete already non existing user
ins = {'userid':1, 'mode':'del'}
x = requests.post(url,json=ins)
print(x.text)

# get all the new users post deleting
x = requests.get(url)
print(x.text)

# edit existing user
ins = {'userid':3, 'name':'EDITED', 'mode':'edit'}
x = requests.post(url,json=ins)
print(x.text)

# edit non existing user
ins = {'userid':1, 'name':'EDITED', 'mode':'edit'}
x = requests.post(url,json=ins)
print(x.text)

# get all the new users post editing
x = requests.get(url)
print(x.text)

# query with wrong types
ins = {'userid':"3", 'name':'EDITED', 'mode':'edit'}
x = requests.post(url,json=ins)
print(x.text)

ins = {'mail':"lol@xd.mc", 'name':231, 'mode':'add'}
x = requests.post(url,json=ins)
print(x.text)

ins = {'mail':1232, 'name':231, 'mode':'add'}
x = requests.post(url,json=ins)
print(x.text)

ins = {'mail':1232, 'name':"38423", 'mode':'add'}
x = requests.post(url,json=ins)
print(x.text)

ins = {'userid':"three", 'mode':'del'}
x = requests.post(url,json=ins)
print(x.text)

# query with wrong email
ins = {'mail':"233@ej", 'name':231, 'mode':'add'}
x = requests.post(url,json=ins)
print(x.text)

ins = {'mail':"skdfkjf", 'name':231, 'mode':'add'}
x = requests.post(url,json=ins)
print(x.text)

# insert with invalid mode
ins = {'mode':'jdfkjd'}
x = requests.post(url,json=ins)
print(x.text)

# insert with missing name
ins = {'mail':'d@d.c', 'mode':'add'}
x = requests.post(url,json=ins)
print(x.text)

ins = {'mail':333, 'mode':'add'}
x = requests.post(url,json=ins)
print(x.text)

# insert with missing email
ins = {'name':"kkk", 'mode':'add'}
x = requests.post(url,json=ins)
print(x.text)

ins = {'name':333, 'mode':'add'}
x = requests.post(url,json=ins)
print(x.text)

# insert with no attrs
ins = {}
x = requests.post(url,json=ins)
print(x.text)

ins = {'mode':'add'}
x = requests.post(url,json=ins)
print(x.text)
ins = {'mode':'edit'}
x = requests.post(url,json=ins)
print(x.text)
ins = {'mode':'del'}
x = requests.post(url,json=ins)
print(x.text)

# insert with faulty mail (3 triues)
ins = {'mail':333, 'mode':'add'}
x = requests.post(url,json=ins)
print(x.text)
ins = {'mail':'sdhfkjshdkfj', 'mode':'add'}
x = requests.post(url,json=ins)
print(x.text)
ins = {'mail':'33@22@34.dsd@', 'mode':'add'}
x = requests.post(url,json=ins)
print(x.text)

# insert with both non string
ins = {'mail':2343, 'name':23434, 'mode':'add'}
x = requests.post(url,json=ins)
print(x.text)


ins = {'name':23434, 'mode':'edit'}
x = requests.post(url,json=ins)
print(x.text)

ins = {'mail':'a.a@a.a', 'name':"dfdfd",'userid':2, 'mode':'edit'}
x = requests.post(url,json=ins)
print(x.text)

x = requests.get(url)
print(x.text)

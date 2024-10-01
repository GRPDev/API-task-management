import requests, json

# Base URL for your API
BASE_URL = 'http://127.0.0.1:8000/app/'

with open('user_data.json', 'r') as f:
    user_data = json.load(f)
with open('user_data2.json', 'r') as f:
    user_data2 = json.load(f)    

# User details
user_data = {
    'username': user_data['username'],
    'password': user_data['password'],
}
user_data2 = {
    'username': user_data2['username'],
    'password': user_data2['password'],
}

# Endpoint URL
endpoint = BASE_URL + 'login/'

# Send POST request to create user
#response = requests.post(endpoint, data=user_data)
headers = {'Content-Type': 'application/json'}
response = requests.post(endpoint, json=user_data, headers=headers)

#get token, update dict and save in file
token = response.json().get('token') #token is a str
user_data['token'] = token
with open('user_data.json', 'w') as file:
    json.dump(user_data, file)

if response.status_code == 200:
    print('200')
    print('Response:', response.json())
else:
    print('Failed to log in.')
    print('Status Code:', response.status_code)
    print('Response:', response.json())

headers2 = {'Content-Type': 'application/json'}
response2 = requests.post(endpoint, json=user_data2, headers=headers2)

#get token, update dict and save in file
token2 = response2.json().get('token') #token is a str
user_data2['token'] = token2
with open('user_data2.json', 'w') as file:
    json.dump(user_data2, file)

# Check the response
if response2.status_code == 200:
    print('200')
    print('Response:', response2.json())
else:
    print('Failed to log in.')
    print('Status Code:', response2.status_code)
    print('Response:', response2.json())
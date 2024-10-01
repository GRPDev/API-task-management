import requests, json
from datetime import datetime, timedelta

# The base URL of your API
#BASE_URL = 'http://127.0.0.1:8000/app/'
BASE_URL = 'http://159.223.7.214/app/' #prod


with open('user_data.json', 'r') as file:
    user_data = json.load(file)

token = user_data['token']

# The headers including the token
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

# Example data for creating a task
data = {
    'executor': 815,  # The ID of the executor user
    'name': 'Test Task via Python 10',
    'cost': 555,
    #'deadline': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    'deadline': (datetime.now() + timedelta(days=-7)).strftime('%Y-%m-%dT%H:%M:%SZ')
}

# Sending the POST request to create the task
response = requests.post(BASE_URL + 'task/create/', headers=headers, json=data)

# Check the response
if response.status_code == 201:
    print('Task created successfully:', response.json())
else:
    print('Failed to create task:', response.status_code, response.json())
    #print(f'Sent data: {data}')
import requests, json
from datetime import datetime, timedelta

# The base URL of your API
BASE_URL = 'http://127.0.0.1:8000/app/'

with open('user_data.json', 'r') as file:
    user_data = json.load(file)

token = user_data['token']

# The headers including the token
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

# Sending the PATCH request to create the task
response = requests.patch(BASE_URL + 'become-executor//', headers=headers) #use <int:task_id>

# Check the response
if response.status_code == 201:
    print('Task created successfully:', response.json())
else:
    print('Failed to create task:', response.status_code, response.json())
    #print(f'Sent data: {data}')
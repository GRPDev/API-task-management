import requests, json
from datetime import datetime, timedelta

# The base URL of your API
BASE_URL = 'http://127.0.0.1:8000/app/'
#BASE_URL = 'http://159.223.7.214/app/' #prod

with open('user_data2.json', 'r') as file:
    user_data = json.load(file)

token = user_data['token']

# The headers including the token
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

# Sending the PATCH request to create the task
response = requests.patch(BASE_URL + 'mark-task-done/282/', headers=headers) #use <int:task_id>

# Check the response
if response.status_code == 200:
    print('Task updated successfully:', response.json())
else:
    print('Failed to update task:', response.status_code, response.json())
    
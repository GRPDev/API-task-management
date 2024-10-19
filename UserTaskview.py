import requests, json

# The base URL of your API
#BASE_URL = 'http://127.0.0.1:8000/app/'
BASE_URL = 'http://159.223.7.214/app/' #prod

# The token for authentication (replace with the actual token)
with open('user_data2.json', 'r') as file:
    user_data2 = json.load(file)

token = user_data2['token']

# The headers including the token
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

# Sending the POST request to create the task
response = requests.get(BASE_URL + 'user-tasks/', headers=headers)

# Check the response
if response.status_code == 200:
    print('Tasks by user:', response.json())
else:
    print('Failed to view tasks by user:', response.status_code, response.json())
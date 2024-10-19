import requests, json

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

# Sending the POST request to create the task
response = requests.get(BASE_URL + 'user-tasks-stats/', headers=headers)

# Check the response
if response.status_code == 200:
    print(response.status_code, 'Success:',response.json())
else:
    print('Failed:', response.status_code, response.json())
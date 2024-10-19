import requests

# The base URL of your API
#BASE_URL = 'http://127.0.0.1:8000/app/'
BASE_URL = 'http://159.223.7.214/app/' #prod

# Sending the POST request to create the task
response = requests.get(BASE_URL + 'task/executor/')

# Check the response
if response.status_code == 200:
    print('Task list:', response.json())
else:
    print('Failed to view tasks:', response.status_code, response.json())
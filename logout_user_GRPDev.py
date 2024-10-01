import requests, json

# logout endpoint 
logout_url = "http://127.0.0.1:8000/app/logout/"

with open('user_data.json', 'r') as f:
    user_data = json.load(f)

# Replace 'your_token_here' with the actual token of the user
headers = {
    "Authorization": user_data['token']
}

response = requests.post(logout_url, headers=headers)

if response.status_code == 200:
    print("Logout successful")
else:
    print(f"Logout failed: {response.status_code}")
import requests, json

# Base URL for your API
BASE_URL = 'http://127.0.0.1:8000/app/'
#BASE_URL = 'http://159.223.7.214/app/' #prod

# User details
user_data = {
    'username': 'GRPDev',
    'password': 'pass1234',
    'email': 'GRPDev@test.com'
}
user_data2 = {
    'username': 'executor',
    'password': 'pass1234',
    'email': 'executor@test.com'
}


# Endpoint URL
endpoint = BASE_URL + 'user/create/'

def create_user():
    # Send POST request to create user
    response = requests.post(endpoint, data=user_data)

    # Check the response
    if response.status_code == 201:
        with open('user_data.json', 'w') as f:
            json.dump(user_data, f)  # Save the user data in a file for later use
        print(f'saved {user_data}' )  
        print("User data saved to 'user_data.json'")
        print('201')
        print('Response:', response.json())
        return response.json()
    else:
        print('Failed to create user.')
        print('Status Code:', response.status_code)
        print('Response:', response.json())
        return None

def create_user2():   
    response2 = requests.post(endpoint, data=user_data2)
    if response2.status_code == 201:
        with open('user_data2.json', 'w') as f:
            json.dump(user_data2, f)
        print(f'saved {user_data2}' ) 
        print("User data saved to 'user_data2.json'")
        print('201')
        print('Response:', response2.json())
        return response2.json()
    else:
        print('Failed to create user.')
        print('Status Code:', response2.status_code)
        print('Response:', response2.json())
        return None
    
create_user()
create_user2()
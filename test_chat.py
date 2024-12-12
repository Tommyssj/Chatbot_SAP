import requests

# URL of the Flask app
url = "http://127.0.0.1:5000/chat"

# Data to send in the POST request
data = {
    "message": "Hello, assistant!"
}

# Send the POST request to the Flask app
response = requests.post(url, json=data)

# Print the response
if response.status_code == 200:
    print("Response JSON:", response.json())
else:
    print(f"Error: {response.status_code}")
    print("Response Text:", response.text)

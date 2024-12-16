import requests
import json

# Define the input data as a list
input_data = [5,166,72,19,175,25.8,0.587,51]


# Convert the input data to a JSON string
input_data_json = json.dumps({"data": [input_data]})

# Replace with the URL of your deployed service
scoring_uri = "http://525b4406-6a85-4a2e-b1b8-218ed866b04c.francecentral.azurecontainer.io/score"

# Define the content type
headers = {"Content-Type": "application/json"}

# Send an HTTP POST request to the endpoint
response = requests.post(scoring_uri, data=input_data_json, headers=headers)

# Check the response status code
if response.status_code == 200:
    # Parse the JSON response
    result = json.loads(response.json())
    print(result)
    # Extract the prediction (result) from the response
    prediction = result["result"][0]
    print(f"Prediction: {prediction}")
else:
    print(f"Error: {response.text}")
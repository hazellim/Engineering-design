import requests

# Replace these values with your own Bridge IP address and API token
bridge_ip = "your_bridge_ip"
api_token = "your_api_token"

# Define the base URL for Hue API requests
base_url = f"http://{bridge_ip}/api/{api_token}"

# Function to send an HTTP GET request to the Hue Bridge
def get_request(endpoint):
    url = f"{base_url}/{endpoint}"
    response = requests.get(url)
    return response.json()

# Function to send an HTTP PUT request to the Hue Bridge
def put_request(endpoint, data):
    url = f"{base_url}/{endpoint}"
    response = requests.put(url, json=data)
    return response.json()

# Example 1: Get the state of a specific light
light_id = 1
light_state = get_request(f"lights/{light_id}")
print(f"State of Light {light_id}: {light_state}")

# Example 2: Turn a light on
light_id = 2
light_state_on = {"on": True}
response = put_request(f"lights/{light_id}/state", light_state_on)
print(f"Turned on Light {light_id}: {response}")

# Example 3: Change the brightness and color of a light
light_id = 3
light_state_changes = {
    "bri": 150,     # Brightness (0-254)
    "hue": 25000,   # Hue (0-65535)
    "sat": 200,     # Saturation (0-254)
}
response = put_request(f"lights/{light_id}/state", light_state_changes)
print(f"Changed Light {light_id} state: {response}")

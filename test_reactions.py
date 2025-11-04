import requests

BASE_URL = "http://localhost:8000/api/messages"

# Test the get_reactions endpoint
def test_get_reactions(message_id):
    url = f"{BASE_URL}/{message_id}/reactions"
    response = requests.get(url)

    if response.status_code == 200:
        print("Reactions retrieved successfully:", response.json())
    else:
        print(f"Failed to retrieve reactions: {response.status_code}", response.text)

if __name__ == "__main__":
    test_get_reactions(1)  # Replace with the valid message_id
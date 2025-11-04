import requests

BASE_URL = "http://localhost:8000/api/messages"

# Test the get_reactions endpoint for a direct message
def test_get_reactions_dm(message_id):
    url = f"{BASE_URL}/{message_id}/reactions"
    response = requests.get(url)

    if response.status_code == 200:
        print("Reactions retrieved successfully for DM:", response.json())
    else:
        print(f"Failed to retrieve reactions for DM: {response.status_code}", response.text)

if __name__ == "__main__":
    test_get_reactions_dm(1)  # Replace with a valid direct message ID
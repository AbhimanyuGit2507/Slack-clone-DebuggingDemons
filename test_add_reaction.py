import requests

BASE_URL = "http://localhost:8000/api/messages"

# Test the add_reaction endpoint
def test_add_reaction(message_id, emoji):
    url = f"{BASE_URL}/{message_id}/reactions"
    payload = {
        "message_id": message_id,  # Include message_id in the payload
        "emoji": emoji
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Reaction added successfully:", response.json())
    else:
        print(f"Failed to add reaction: {response.status_code}", response.text)

if __name__ == "__main__":
    test_add_reaction(1, "👍")  # Replace with the valid message_id and emoji
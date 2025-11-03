#!/usr/bin/env python3
"""
Simple test script for Slack Clone Backend API
This script demonstrates basic API functionality with test data
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

class SlackCloneAPITester:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.current_user = None
        self.test_users = []
        self.test_channels = []
        
    def print_section(self, title):
        """Print a formatted section header"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print('='*60)
    
    def print_response(self, response, action):
        """Print response details"""
        print(f"\n{action}")
        print(f"Status: {response.status_code}")
        if response.status_code < 400:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    
    def signup(self, username, email, password):
        """Sign up a new user"""
        url = f"{self.base_url}/auth/signup"
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        response = self.session.post(url, json=data)
        self.print_response(response, f"Signing up user: {username}")
        
        if response.status_code == 201:
            self.current_user = response.json()['user']
            self.test_users.append(self.current_user)
        
        return response
    
    def login(self, username, password):
        """Login an existing user"""
        url = f"{self.base_url}/auth/login"
        data = {
            "username": username,
            "password": password
        }
        response = self.session.post(url, json=data)
        self.print_response(response, f"Logging in user: {username}")
        
        if response.status_code == 200:
            self.current_user = response.json()['user']
        
        return response
    
    def get_me(self):
        """Get current user info"""
        url = f"{self.base_url}/auth/me"
        response = self.session.get(url)
        self.print_response(response, "Getting current user")
        return response
    
    def create_channel(self, name, description=None, is_private=False):
        """Create a new channel"""
        url = f"{self.base_url}/channels"
        data = {
            "name": name,
            "description": description,
            "is_private": is_private
        }
        response = self.session.post(url, json=data)
        self.print_response(response, f"Creating channel: {name}")
        
        if response.status_code == 201:
            self.test_channels.append(response.json())
        
        return response
    
    def list_channels(self):
        """List all channels"""
        url = f"{self.base_url}/channels"
        response = self.session.get(url)
        self.print_response(response, "Listing channels")
        return response
    
    def send_message(self, channel_id, content):
        """Send a message to a channel"""
        url = f"{self.base_url}/messages"
        data = {
            "channel_id": channel_id,
            "user_id": self.current_user['id'],
            "content": content
        }
        response = self.session.post(url, json=data)
        self.print_response(response, f"Sending message to channel {channel_id}")
        return response
    
    def get_channel_messages(self, channel_id):
        """Get messages from a channel"""
        url = f"{self.base_url}/messages/channel/{channel_id}"
        response = self.session.get(url)
        self.print_response(response, f"Getting messages from channel {channel_id}")
        return response
    
    def send_dm(self, receiver_id, content):
        """Send a direct message"""
        url = f"{self.base_url}/direct-messages"
        data = {
            "receiver_id": receiver_id,
            "content": content
        }
        response = self.session.post(url, json=data)
        self.print_response(response, f"Sending DM to user {receiver_id}")
        return response
    
    def add_reaction(self, message_id, emoji):
        """Add a reaction to a message"""
        url = f"{self.base_url}/messages/{message_id}/reactions"
        data = {
            "message_id": message_id,
            "emoji": emoji
        }
        response = self.session.post(url, json=data)
        self.print_response(response, f"Adding reaction {emoji} to message {message_id}")
        return response
    
    def create_thread(self, message_id, content):
        """Create a thread reply"""
        url = f"{self.base_url}/messages/{message_id}/threads"
        data = {
            "parent_message_id": message_id,
            "content": content
        }
        response = self.session.post(url, json=data)
        self.print_response(response, f"Creating thread reply to message {message_id}")
        return response
    
    def list_users(self):
        """List all users"""
        url = f"{self.base_url}/users"
        response = self.session.get(url)
        self.print_response(response, "Listing all users")
        return response
    
    def logout(self):
        """Logout current user"""
        url = f"{self.base_url}/auth/logout"
        response = self.session.post(url)
        self.print_response(response, "Logging out")
        self.current_user = None
        return response


def run_tests():
    """Run a comprehensive test suite"""
    tester = SlackCloneAPITester()
    
    # Test 1: User Registration and Authentication
    tester.print_section("TEST 1: User Registration & Authentication")
    tester.signup("alice", "alice@example.com", "password123")
    tester.get_me()
    
    # Test 2: Create Channels
    tester.print_section("TEST 2: Create Channels")
    tester.create_channel("general", "General discussion", False)
    tester.create_channel("random", "Random stuff", False)
    tester.create_channel("private-team", "Team channel", True)
    tester.list_channels()
    
    # Test 3: Send Messages
    tester.print_section("TEST 3: Send Messages")
    if tester.test_channels:
        channel_id = tester.test_channels[0]['id']
        tester.send_message(channel_id, "Hello everyone! 👋")
        tester.send_message(channel_id, "This is a test message")
        tester.get_channel_messages(channel_id)
    
    # Test 4: Create second user
    tester.print_section("TEST 4: Create Second User")
    tester.signup("bob", "bob@example.com", "password456")
    
    # Test 5: Direct Messages
    tester.print_section("TEST 5: Direct Messages")
    if len(tester.test_users) > 1:
        tester.send_dm(tester.test_users[0]['id'], "Hey Alice!")
    
    # Test 6: Switch back to first user
    tester.print_section("TEST 6: Switch Users & Test Reactions")
    tester.logout()
    tester.login("alice", "password123")
    
    # Add reaction to message
    if tester.test_channels:
        channel_id = tester.test_channels[0]['id']
        messages_response = tester.get_channel_messages(channel_id)
        if messages_response.status_code == 200:
            messages = messages_response.json()
            if messages:
                message_id = messages[0]['id']
                tester.add_reaction(message_id, "👍")
                tester.create_thread(message_id, "Great message!")
    
    # Test 7: List Users
    tester.print_section("TEST 7: User Directory")
    tester.list_users()
    
    # Test 8: Logout
    tester.print_section("TEST 8: Logout")
    tester.logout()
    
    print("\n" + "="*60)
    print("  All tests completed!")
    print("="*60)
    print(f"\nCreated {len(tester.test_users)} test users")
    print(f"Created {len(tester.test_channels)} test channels")
    print("\nYou can now explore the API at http://localhost:8000/docs")


if __name__ == "__main__":
    print("Slack Clone Backend API Tester")
    print("Make sure the backend server is running on http://localhost:8000")
    
    try:
        run_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to the backend server")
        print("Please make sure the backend is running:")
        print("  uvicorn backend.main:app --reload --port 8000")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

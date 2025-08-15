#!/usr/bin/env python
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_mailtrap_api():
    token = os.getenv('MAILTRAP_TOKEN')
    
    print(f"Testing con token: {token[:8]}...")
    
    # Test 1: Sending API
    print("\n=== TEST SENDING API ===")
    url_sending = "https://send.api.mailtrap.io/api/send"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "from": {
            "email": "test@example.com",
            "name": "Test"
        },
        "to": [{"email": "recipient@example.com"}],
        "subject": "Test",
        "text": "Test message"
    }
    
    try:
        response = requests.post(url_sending, headers=headers, data=json.dumps(data))
        print(f"Sending API - Status: {response.status_code}")
        print(f"Sending API - Response: {response.text}")
    except Exception as e:
        print(f"Sending API - Error: {e}")
    
    # Test 2: Sandbox API (necesita inbox ID)
    print("\n=== TEST SANDBOX API ===")
    inbox_id = os.getenv('MAILTRAP_INBOX_ID', '2835764')
    url_sandbox = f"https://sandbox.api.mailtrap.io/api/send/{inbox_id}"
    
    try:
        response = requests.post(url_sandbox, headers=headers, data=json.dumps(data))
        print(f"Sandbox API - Status: {response.status_code}")
        print(f"Sandbox API - Response: {response.text}")
    except Exception as e:
        print(f"Sandbox API - Error: {e}")

if __name__ == "__main__":
    test_mailtrap_api()

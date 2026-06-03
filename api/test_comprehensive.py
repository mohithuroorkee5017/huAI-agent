"""
Comprehensive API Test - Verifies all fixed functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_scenario(title, payload):
    """Test an API scenario"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)
    print(f"Request: {json.dumps(payload, ensure_ascii=False)}")
    
    try:
        response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=30)
        print(f"Status: {response.status_code}")
        
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Language: {data.get('language')}")
        print(f"Response: {data.get('answer', '')[:150]}...")
        print(f"Sources: {len(data.get('sources', []))} found")
        
        if data.get('success'):
            print("✓ PASS")
            return True
        else:
            print(f"✗ FAIL: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

# Test scenarios from requirements
print("\n" + "#"*70)
print("# COMPREHENSIVE API TESTING - All Scenarios")
print("#"*70)

results = []

# Scenario 1: Exact requirement - Hinglish message
results.append(test_scenario(
    "Requirement Scenario: Hinglish Message",
    {
        "conversation_id": "conv_123",
        "message": "Hello bhai kaise ho"
    }
))

# Scenario 2: English message
results.append(test_scenario(
    "English Message",
    {
        "conversation_id": "conv_en_001",
        "message": "What is the placement package at the university?"
    }
))

# Scenario 3: Continue with follow-up
time.sleep(1)
results.append(test_scenario(
    "Follow-up English Message (Same Conversation)",
    {
        "conversation_id": "conv_en_001",
        "message": "Tell me about top recruiters"
    }
))

# Scenario 4: Knowledge Base Query
time.sleep(1)
results.append(test_scenario(
    "Knowledge Base Query",
    {
        "conversation_id": "conv_kb_001",
        "message": "Tell me about hostel facilities and fees"
    }
))

# Test endpoints
print("\n" + "#"*70)
print("# ENDPOINT TESTS")
print("#"*70)

print("\n1. Testing GET /health...")
try:
    resp = requests.get(f"{BASE_URL}/health")
    health = resp.json()
    print(f"   Status: {health['status']}")
    print(f"   Version: {health['version']}")
    print(f"   ✓ PASS")
except Exception as e:
    print(f"   ✗ FAIL: {e}")

print("\n2. Testing GET /status...")
try:
    resp = requests.get(f"{BASE_URL}/status")
    status = resp.json()
    print(f"   Status: {status['status']}")
    print(f"   API Configured: {status['api_configured']}")
    print(f"   Active Conversations: {status['active_conversations']}")
    print(f"   ✓ PASS")
except Exception as e:
    print(f"   ✗ FAIL: {e}")

# Summary
print("\n" + "#"*70)
print("# TEST SUMMARY")
print("#"*70)
passed = sum(results)
total = len(results)
print(f"\nChat Tests: {passed}/{total} passed")
print(f"Success Rate: {(passed/total)*100:.1f}%")

if passed == total:
    print("\n🎉 ALL TESTS PASSED!")
else:
    print(f"\n⚠ {total - passed} test(s) failed")

print("\n" + "#"*70)
print("# TESTING COMPLETE")
print("#"*70)

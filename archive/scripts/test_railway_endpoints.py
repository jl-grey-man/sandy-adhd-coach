import requests
import json

BASE_URL = "https://sandy-adhd-coach-production.up.railway.app"

print("=" * 80)
print("RAILWAY API ENDPOINT VERIFICATION")
print("=" * 80)

# First, login to get token
print("\n1. Testing login...")
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "user@example.com", "password": "string"}
)

if response.status_code == 200:
    token = response.json()["token"]
    print("✅ Login successful")
    print(f"   Token: {token[:50]}...")
else:
    print(f"❌ Login failed: {response.status_code}")
    print(f"   {response.text}")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

# Test get-prompt endpoint
print("\n2. Testing GET /chat/get-prompt...")
response = requests.get(f"{BASE_URL}/chat/get-prompt", headers=headers)

if response.status_code == 200:
    prompt = response.json()["prompt"]
    print("✅ Get prompt successful")
    print(f"   Prompt length: {len(prompt)} characters")
    print(f"   First 200 chars: {prompt[:200]}...")
else:
    print(f"❌ Get prompt failed: {response.status_code}")
    print(f"   {response.text}")

# Test update-prompt endpoint
print("\n3. Testing POST /chat/update-prompt...")
test_prompt = "This is a test custom prompt update"
response = requests.post(
    f"{BASE_URL}/chat/update-prompt",
    headers=headers,
    json={"prompt": test_prompt}
)

if response.status_code == 200:
    print("✅ Update prompt successful")
    print(f"   Message: {response.json().get('message')}")
    
    # Verify the update
    print("\n4. Verifying prompt was updated...")
    response = requests.get(f"{BASE_URL}/chat/get-prompt", headers=headers)
    if response.status_code == 200:
        updated_prompt = response.json()["prompt"]
        if test_prompt in updated_prompt or "custom_system_prompt" in str(updated_prompt):
            print("✅ Prompt update verified")
        else:
            print("⚠️  Prompt may not have been updated correctly")
            print(f"   Updated prompt: {updated_prompt[:200]}...")
else:
    print(f"❌ Update prompt failed: {response.status_code}")
    print(f"   {response.text}")

# Test other important endpoints
print("\n5. Testing POST /chat/message...")
response = requests.post(
    f"{BASE_URL}/chat/message",
    headers=headers,
    json={"message": "test message", "session_id": "test_session"}
)

if response.status_code == 200:
    print("✅ Chat message successful")
else:
    print(f"❌ Chat message failed: {response.status_code}")
    print(f"   {response.text}")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)

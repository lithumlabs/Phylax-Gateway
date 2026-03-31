import requests

# 🚨 ඔයාගේ 8080 පෝර්ට් එකේ අලුත්ම Public URL එක මෙතනට දාන්න
# උදා: https://congenial-umbrella-xxxx-8080.app.github.dev/api/pay
GATEWAY_URL = "https://congenial-umbrella-wr6xwr9pj465h79g-8080.app.github.dev/api/pay"

def test_gateway(api_key, site_url):
    payload = {
        "api_key": api_key,
        "site_url": site_url
    }
    
    print(f"🚀 Sending request for {site_url} using key: {api_key}...")
    
    try:
        response = requests.post(GATEWAY_URL, json=payload)
        if response.status_code == 200:
            print("✅ SUCCESS: Access Granted!")
        elif response.status_code == 403:
            print("🚫 BLOCKED: Unauthorized Key detected!")
        elif response.status_code == 402:
            print(f"⚠️ DENIED: {response.json().get('reason')}")
        else:
            print(f"❌ ERROR {response.status_code}: {response.text}")
    except Exception as e:
        print(f"🔥 Critical Error: {str(e)}")

# --- පරීක්ෂණ කිහිපයක් කරමු ---

# 1. නිවැරදි API Key එකක් (අපි කලින් SQL එකෙන් දාපු එක)
print("\n--- Test 1: Valid Bot ---")
test_gateway("sk-test-123", "https://physicsguru.ai")

# 2. වැරදි (හොර) API Key එකක්
print("\n--- Test 2: Fake/Unauthorized Bot ---")
test_gateway("sk-hacker-99", "https://premium-data.com")
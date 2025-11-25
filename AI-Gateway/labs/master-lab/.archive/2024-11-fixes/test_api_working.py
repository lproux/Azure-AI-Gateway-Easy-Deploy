#!/usr/bin/env python3
"""
Test if API is working after removing broken semantic caching policy
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI
import time

# Load environment
env_file = Path('master-lab.env')
load_dotenv(env_file)

apim_gateway_url = os.environ.get('APIM_GATEWAY_URL')
apim_api_key = os.environ.get('APIM_API_KEY')
inference_api_path = os.environ.get('INFERENCE_API_PATH', 'inference')

print("=" * 80)
print("🧪 TESTING API AFTER POLICY RESTORE")
print("=" * 80)
print(f"\nEndpoint: {apim_gateway_url}/{inference_api_path}")
print(f"Model: gpt-4o-mini\n")

# Wait a bit for policy propagation
print("[*] Waiting 15 seconds for policy to propagate...")
time.sleep(15)

client = AzureOpenAI(
    azure_endpoint=f"{apim_gateway_url}/{inference_api_path}",
    api_key=apim_api_key,
    api_version="2025-03-01-preview"
)

print("\n[*] Making test request...")
start_time = time.time()

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Say 'API is working!' if you receive this message."}
        ],
        max_tokens=50
    )
    response_time = time.time() - start_time

    print(f"\n✅ API Request Successful!")
    print(f"   Response Time: {response_time:.2f}s")
    print(f"   Response: {response.choices[0].message.content}")
    print("\n🎉 The 500 errors are fixed! API is operational.")

except Exception as e:
    print(f"\n❌ API Still Failing")
    print(f"   Error: {str(e)[:200]}")
    print("\n💡 The policy may need more time to propagate (wait 60 seconds)")
    print("   OR there may be other issues beyond the semantic caching policy")

print("\n" + "=" * 80)

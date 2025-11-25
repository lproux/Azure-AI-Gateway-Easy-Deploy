#!/usr/bin/env python3
"""
Test semantic caching functionality after re-enabling
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
print("🧪 TESTING SEMANTIC CACHING")
print("=" * 80)
print(f"\nEndpoint: {apim_gateway_url}/{inference_api_path}")
print(f"Model: gpt-4o-mini\n")

# Wait for policy propagation
print("[*] Waiting 30 seconds for policy to propagate...")
time.sleep(30)

client = AzureOpenAI(
    azure_endpoint=f"{apim_gateway_url}/{inference_api_path}",
    api_key=apim_api_key,
    api_version="2025-03-01-preview"
)

# Test with similar questions
questions = [
    "How to brew coffee?",
    "What are the steps to make coffee?",
    "How do I brew the perfect cup of coffee?"
]

print("\n" + "=" * 80)
print("TEST: Making 3 similar requests")
print("=" * 80)
print("Expected behavior:")
print("  1st request: Slow (~3-10s) - backend call + embedding + cache store")
print("  2nd request: Fast (~0.1-0.3s) - cache hit")
print("  3rd request: Fast (~0.1-0.3s) - cache hit")
print("\n")

results = []

for i, question in enumerate(questions, 1):
    print(f"▶️ Request {i}/3: {question}")

    start_time = time.time()
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": question}
            ],
            max_tokens=100
        )
        response_time = time.time() - start_time

        status = "🎯 CACHE HIT" if response_time < 1.0 else "🔥 BACKEND CALL"
        print(f"   ⏱️  {response_time:.2f}s - {status}")

        results.append(response_time)

    except Exception as e:
        print(f"   ❌ Error: {str(e)[:150]}")
        results.append(None)

    # Small delay between requests
    time.sleep(0.5)

print("\n" + "=" * 80)
print("RESULTS")
print("=" * 80)

if all(r is not None for r in results):
    print(f"Request 1: {results[0]:.2f}s (first call)")
    print(f"Request 2: {results[1]:.2f}s (should be cached)")
    print(f"Request 3: {results[2]:.2f}s (should be cached)")

    # Check if caching is working
    if results[0] > 1.0 and results[1] < 1.0 and results[2] < 1.0:
        speedup = results[0] / results[1]
        print(f"\n✅ SEMANTIC CACHING IS WORKING!")
        print(f"   First request: {results[0]:.2f}s (backend)")
        print(f"   Cached requests: ~{(results[1] + results[2])/2:.2f}s (average)")
        print(f"   Speed improvement: {speedup:.1f}x faster!")
        print("\n🎉 Semantic caching is successfully enabled and functional!")
    else:
        print(f"\n⚠️  Caching may not be working as expected")
        print("   Possible reasons:")
        print("   - Policy still propagating (wait 60 seconds total)")
        print("   - Questions not similar enough (need >80% match)")
        print("   - Redis connection issue")
        print("\n💡 Try running cells 53-54 in the notebook for a full test")
else:
    print("\n❌ Some requests failed")
    print("   Check the errors above for details")

print("\n" + "=" * 80)

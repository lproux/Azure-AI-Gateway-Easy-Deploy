"""
Test script to verify load balancing is working correctly
"""

import os
import time
import requests
from collections import Counter
from dotenv import load_dotenv

def test_load_balancing():
    """Test that requests are being distributed across backends"""

    # Load environment variables
    env_file = 'master-lab.env'
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print(f"[OK] Loaded environment from {env_file}")

    # Get configuration
    apim_gateway_url = os.environ.get('APIM_GATEWAY_URL')
    inference_api_path = os.environ.get('INFERENCE_API_PATH', 'inference')
    apim_api_key = os.environ.get('APIM_API_KEY')
    api_version = os.environ.get('OPENAI_API_VERSION', '2024-06-01')

    if not all([apim_gateway_url, apim_api_key]):
        print("[ERROR] Missing required environment variables")
        return

    print("="*80)
    print("TESTING LOAD BALANCING")
    print("="*80)
    print()
    print(f"Gateway URL: {apim_gateway_url}")
    print(f"API Path: {inference_api_path}")
    print()

    # Make test requests
    num_requests = 10
    print(f"[*] Making {num_requests} test requests...")
    print()

    regions = []
    backend_ids = []
    response_times = []
    errors = []

    for i in range(num_requests):
        start = time.time()

        try:
            url = f"{apim_gateway_url.rstrip('/')}/{inference_api_path}/openai/deployments/gpt-4o-mini/chat/completions"

            response = requests.post(
                url=f"{url}?api-version={api_version}",
                headers={
                    "api-key": apim_api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "messages": [{"role": "user", "content": f"Test request {i+1}: Hello"}],
                    "max_tokens": 5,
                    "temperature": 0
                },
                timeout=30
            )

            elapsed = time.time() - start
            response_times.append(elapsed)

            # Get region and backend info from headers
            region = response.headers.get('x-ms-region', 'Unknown')
            backend_id = response.headers.get('x-ms-backend-id', 'Unknown')

            regions.append(region)
            backend_ids.append(backend_id)

            if response.status_code == 200:
                print(f"Request {i+1:2}: ✓ {elapsed:.2f}s - Region: {region:15} - Backend: {backend_id}")
            else:
                print(f"Request {i+1:2}: ✗ HTTP {response.status_code} - {elapsed:.2f}s")
                errors.append(f"HTTP {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Request {i+1:2}: ✗ Error: {str(e)[:50]}")
            errors.append(str(e)[:50])
            regions.append('Error')
            backend_ids.append('Error')
            response_times.append(0)

        # Small delay between requests
        time.sleep(0.5)

    print()
    print("="*80)
    print("RESULTS SUMMARY")
    print("="*80)
    print()

    # Analyze distribution
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        print(f"Average response time: {avg_time:.2f}s")

    print()
    print("Region Distribution:")
    region_counts = Counter(regions)
    for region, count in region_counts.items():
        pct = (count / len(regions) * 100)
        print(f"  {region:20}: {count:2} requests ({pct:5.1f}%)")

    print()
    print("Backend Distribution:")
    backend_counts = Counter(backend_ids)
    for backend, count in backend_counts.items():
        pct = (count / len(backend_ids) * 100)
        print(f"  {backend:20}: {count:2} requests ({pct:5.1f}%)")

    if errors:
        print()
        print(f"Errors: {len(errors)} requests failed")
        for error in set(errors):
            print(f"  - {error}")

    print()

    # Determine if load balancing is working
    unique_regions = [r for r in set(regions) if r not in ['Unknown', 'Error']]
    unique_backends = [b for b in set(backend_ids) if b not in ['Unknown', 'Error', 'unknown']]

    print("="*80)
    print("DIAGNOSIS")
    print("="*80)
    print()

    if len(unique_backends) > 1 or len(unique_regions) > 1:
        print("✓ LOAD BALANCING IS WORKING!")
        print(f"  Requests distributed across {len(unique_backends)} backends")
        if 'foundry1' in backend_ids and backend_counts['foundry1'] == len(backend_ids):
            print("  All traffic going to Priority 1 (UK South) - this is correct behavior")
            print("  Lower priority backends will only be used if UK South fails")
    else:
        print("✗ LOAD BALANCING IS NOT WORKING")
        print("  All requests going to the same backend")
        print()
        print("TROUBLESHOOTING STEPS:")
        print("1. Run the backend pool fix script first")
        print("2. Ensure Cell 43 (policy update) has been executed")
        print("3. Check that backends are created in APIM portal")
        print("4. Verify the backend pool exists in APIM")

        if all(r == 'Unknown' for r in regions):
            print()
            print("NOTE: Region headers are not being set")
            print("This doesn't affect load balancing but makes debugging harder")

    print()
    print("="*80)
    print("TEST COMPLETE")
    print("="*80)
    print()

if __name__ == "__main__":
    test_load_balancing()
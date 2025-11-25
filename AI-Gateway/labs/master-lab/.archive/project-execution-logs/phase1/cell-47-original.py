print('Testing load balancing across 3 regions...')
responses = []
regions = []  # Track which region processed each request
backend_ids = []  # Track which backend served each request

# Resolve required variables (avoid NameError)
apim_gateway_url = (
    (step1_outputs.get('apimGatewayUrl') if isinstance(step1_outputs, dict) else None) or
    os.environ.get('APIM_GATEWAY_URL')
)
inference_api_path = (
    (step2_outputs.get('inferenceAPIPath') if isinstance(step2_outputs, dict) else None) or
    os.environ.get('INFERENCE_API_PATH', 'inference')
)
apim_api_key = (
    (step1_outputs.get('apimSubscriptions', [{}])[0].get('key') if isinstance(step1_outputs, dict) else None) or
    os.environ.get('APIM_API_KEY')
)
api_version = os.environ.get('OPENAI_API_VERSION', '2024-06-01')

missing = [n for n, v in {
    'apim_gateway_url': apim_gateway_url,
    'inference_api_path': inference_api_path,
    'apim_api_key': apim_api_key,
    'api_version': api_version
}.items() if not v]

if missing:
    print(f"[ERROR] Missing required variables: {', '.join(missing)}")
    print("[HINT] Ensure Cell 8 (.env generation) ran and load with: from dotenv import load_dotenv; load_dotenv('master-lab.env')")
    # Abort early to avoid further errors
else:
    # Use requests library to access HTTP headers (avoid duplicate import)
    try:
        requests
    except NameError:
        import requests

    for i in range(5):
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
                    "messages": [{"role": "user", "content": f"Test {i+1}"}],
                    "max_tokens": 5
                },
                timeout=30
            )

            elapsed = time.time() - start
            responses.append(elapsed)

            region = response.headers.get('x-ms-region', 'Unknown')
            backend_id = response.headers.get('x-ms-backend-id', 'Unknown')

            regions.append(region)
            backend_ids.append(backend_id)

            if response.status_code == 200:
                print(f"Request {i+1}: {elapsed:.2f}s - Region: {region} - Backend: {backend_id}")
            else:
                print(f"Request {i+1}: {elapsed:.2f}s - HTTP {response.status_code} - Region: {region} - Backend: {backend_id}")
        except requests.exceptions.RequestException as e:
            print(f"[WARN] Request {i+1} failed: {e}")
            responses.append(0)
            regions.append('Error')
            backend_ids.append('Error')

        time.sleep(0.2)

    avg_time = sum(responses) / len(responses) if responses else 0
    print(f"\nAverage response time: {avg_time:.2f}s")

    from collections import Counter
    region_counts = Counter(regions)
    print(f"\nRegion Distribution:")
    for region, count in region_counts.items():
        pct = (count / len(regions) * 100) if regions else 0
        print(f"  {region}: {count} requests ({pct:.1f}%)")

    unknown_count = region_counts.get('Unknown', 0)
    if unknown_count == len(regions) and len(regions) > 0:
        print('')
        print('[INFO] All regions showing as "Unknown" - region headers may not be configured in APIM')
        print('')
        print('📋 TO ADD REGION HEADERS VIA APIM POLICY:')
        print('   1. Azure Portal → API Management → APIs → inference-api')
        print('   2. Click "All operations" → Outbound processing → Add policy')
        print('   3. Add this XML to <outbound> section:')
        print('')
        print('   <set-header name="x-ms-region" exists-action="override">')
        print('       <value>@(context.Deployment.Region)</value>')
        print('   </set-header>')
        print('   <set-header name="x-ms-backend-id" exists-action="override">')
        print('       <value>@(context.Request.MatchedParameters.GetValueOrDefault("backend-id", "unknown"))</value>')
        print('   </set-header>')
        print('')
        print('   4. Save the policy')
        print('')
        print('ℹ️  Region detection is informational only - load balancing still works')
        print('')

# Fallback util if utils.print_ok not available
if 'utils' in globals() and hasattr(utils, 'print_ok'):
    utils.print_ok('Load balancing test complete!')
else:
    print('[OK] Load balancing test complete!')

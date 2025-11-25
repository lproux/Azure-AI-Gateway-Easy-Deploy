"""
Fix for Cell 147: Simplify Image Generation to APIM-Only
Issue: Complex endpoint discovery logic with potential auth issues
Severity: MEDIUM
Solution: Always use APIM gateway for consistency and simplicity
"""

import base64, math

# Image & Vision Model Initialization - SIMPLIFIED to APIM-only approach

IMAGE_MODEL = globals().get('DALL_E_DEPLOYMENT') or os.environ.get('DALL_E_DEPLOYMENT') or 'gpt-image-1'
VISION_MODEL = globals().get('VISION_MODEL') or os.environ.get('VISION_MODEL') or 'gpt-4o'
IMAGE_API_VERSION = globals().get('OPENAI_IMAGE_API_VERSION') or os.environ.get('OPENAI_IMAGE_API_VERSION') or '2025-06-01-preview'
CHAT_API_VERSION = globals().get('OPENAI_CHAT_API_VERSION') or os.environ.get('OPENAI_CHAT_API_VERSION') or '2025-06-01-preview'
DEFAULT_SIZE = globals().get('DALL_E_DEFAULT_SIZE') or os.environ.get('DALL_E_DEFAULT_SIZE') or '1024x1024'
OUTPUT_FORMAT = globals().get('IMAGE_OUTPUT_FORMAT') or os.environ.get('IMAGE_OUTPUT_FORMAT') or 'png'

# SIMPLIFIED: Always use APIM gateway
APIM_BASE = globals().get('APIM_GATEWAY') or os.environ.get('APIM_GATEWAY_URL') or globals().get('apim_gateway_url')
INFERENCE_PATH = globals().get('INFERENCE_PATH') or os.environ.get('INFERENCE_API_PATH') or 'inference'

if not APIM_BASE:
    raise ValueError('APIM_GATEWAY_URL not configured. Cannot initialize image generation.')

ACTIVE_IMAGE_URL = f"{APIM_BASE}/{INFERENCE_PATH}/openai/images/generations?api-version={IMAGE_API_VERSION}"
SOURCE = 'apim'

print(f"[image-init] IMAGE_MODEL={IMAGE_MODEL} | VISION_MODEL={VISION_MODEL}")
print(f"[image-init] Using APIM gateway: {ACTIVE_IMAGE_URL}")

# SIMPLIFIED: Use existing auth headers from earlier cells
# Reuse headers_both or final_headers that were already configured
IMAGE_HEADERS = {}

# Try to reuse existing headers
existing_headers = globals().get('headers_both') or globals().get('final_headers') or {}
if existing_headers:
    IMAGE_HEADERS.update(existing_headers)
    print(f"[image-init] Reusing existing auth headers")
else:
    # Fallback to API key if headers not available
    api_key = globals().get('apim_api_key') or os.environ.get('APIM_API_KEY')
    if api_key:
        IMAGE_HEADERS['api-key'] = api_key
        print(f"[image-init] Using APIM API key authentication")
    else:
        print(f"[image-init] WARNING: No authentication headers available")

# Common content headers
IMAGE_HEADERS['Content-Type'] = 'application/json'

print(f"[image-init] Headers configured: {list(IMAGE_HEADERS.keys())}")

# Generation helper

def generate_image(prompt: str, size: str = DEFAULT_SIZE, model: str = IMAGE_MODEL, debug: bool = True):
    """
    Generate image using Azure OpenAI via APIM gateway.

    Args:
        prompt: Text description of image to generate
        size: Image dimensions (e.g., '1024x1024', '512x512')
        model: Deployment name of image model
        debug: Print debug information

    Returns:
        dict with 'b64' key containing base64 image data, or 'error' key on failure
    """
    if not ACTIVE_IMAGE_URL:
        return {'error': 'No active image endpoint available'}

    payload = {
        'model': model,
        'prompt': prompt,
        'size': size,
        'response_format': 'b64_json'
    }

    start = time.time()
    try:
        r = requests.post(ACTIVE_IMAGE_URL, headers=IMAGE_HEADERS, json=payload, timeout=60)
    except Exception as ex:
        return {'error': f'Exception during POST: {ex}'}

    elapsed = round(time.time() - start, 2)

    if debug:
        print(f"[generate_image] status={r.status_code} elapsed={elapsed}s model={model}")

    if r.status_code != 200:
        try:
            error_detail = r.json()
            return {'error': f'HTTP {r.status_code}', 'details': error_detail, 'elapsed': elapsed, 'source': SOURCE}
        except Exception:
            return {'error': f'HTTP {r.status_code}', 'text': r.text[:500], 'elapsed': elapsed, 'source': SOURCE}

    try:
        data = r.json()
        # Azure OpenAI image format differs across previews; unify extraction
        b64 = None
        if isinstance(data, dict):
            # Common patterns: data -> [ { b64_json: ... } ] or images -> [ { b64_json: ... } ]
            arr = data.get('data') or data.get('images') or []
            if arr and isinstance(arr, list):
                first = arr[0]
                b64 = first.get('b64_json') or first.get('base64_data')

        if not b64:
            return {'error': 'No b64 image found in response', 'raw_keys': list(data.keys()), 'elapsed': elapsed}

        return {'b64': b64, 'elapsed': elapsed, 'source': SOURCE, 'model': model}
    except Exception as ex:
        return {'error': f'Failed to parse JSON: {ex}', 'elapsed': elapsed}

# Vision helper placeholder (to be wired once image path proven)

def analyze_image_base64(b64: str, prompt: str, model: str = VISION_MODEL):
    """Analyze image using vision model - to be implemented"""
    return {'note': 'Vision analysis not yet implemented in this inline section.'}

print("[image-init] ✅ Image generation initialized via APIM gateway")

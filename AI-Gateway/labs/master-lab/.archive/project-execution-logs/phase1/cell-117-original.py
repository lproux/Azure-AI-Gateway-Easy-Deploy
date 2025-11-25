# Validate required environment variables
required_vars = ['RESOURCE_GROUP', 'APIM_GATEWAY_URL']
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"⚠️  Missing environment variables: {missing}")
    print("   Run Cell 3 (Environment Loader) first")
    raise RuntimeError(f"Missing variables: {missing}")

# Updated Lab 22 Image Generation & Vision Analysis (FLUX models with deployment-style routing)
import os, base64, json, requests
from typing import Optional

# Core config
# Provide safe defaults if prior cells defining these globals have not run yet.
if 'IMAGE_API_VERSION' not in globals():
    IMAGE_API_VERSION = os.getenv("OPENAI_IMAGE_API_VERSION", "2024-08-01-preview")
if 'VISION_MODEL' not in globals():
    VISION_MODEL = os.getenv("VISION_MODEL", "gpt-4o-mini")
if 'USE_JWT' not in globals():
    USE_JWT = False
if 'DALL_E_DEFAULT_SIZE' not in globals():
    DALL_E_DEFAULT_SIZE = "1024x1024"
if 'FLUX_DEFAULT_SIZE' not in globals():
    FLUX_DEFAULT_SIZE = "1024x1024"
if 'IMAGE_OUTPUT_FORMAT' not in globals():
    IMAGE_OUTPUT_FORMAT = "png"

inference_api_path = os.getenv("INFERENCE_API_PATH", "inference")
# APIM gateway URL is required; fallback to any existing global if env not set (should be set by validation above)
apim_gateway_url = os.getenv("APIM_GATEWAY_URL") or globals().get("apim_gateway_url", "")
image_api_version = os.getenv("OPENAI_IMAGE_API_VERSION", IMAGE_API_VERSION)
vision_model = os.getenv("VISION_MODEL", VISION_MODEL)
use_jwt = (os.getenv("USE_JWT_FOR_IMAGE", "false").lower() == "true") or USE_JWT

# FIXED: Updated to use FLUX models instead of DALL-E (foundry1 has FLUX.1-Kontext-pro and FLUX-1.1-pro)
image_model = os.getenv("DALL_E_DEPLOYMENT", "FLUX-1.1-pro") or "FLUX-1.1-pro"
flux_model = os.getenv("FLUX_DEPLOYMENT", "FLUX.1-Kontext-pro").strip()

DALL_E_DEFAULT_SIZE = os.getenv("DALL_E_DEFAULT_SIZE", DALL_E_DEFAULT_SIZE)
FLUX_DEFAULT_SIZE = os.getenv("FLUX_DEFAULT_SIZE", FLUX_DEFAULT_SIZE)
IMAGE_OUTPUT_FORMAT = os.getenv("IMAGE_OUTPUT_FORMAT", IMAGE_OUTPUT_FORMAT)

# Compose auth headers
final_headers = {}
if 'headers_both' in globals():
    final_headers.update(headers_both)
elif 'headers' in globals():
    final_headers.update(headers)
if use_jwt and 'access_token' in globals() and access_token:
    final_headers['Authorization'] = f'Bearer {access_token}'

# FIXED: Use deployment-style routing (APIM pattern) instead of model-name style
# Pattern: /deployments/{deployment-id}/images/generations
def generate_image(model_name: str, prompt: str, size: str) -> Optional[str]:
    # Build deployment-style URL with model_name as deployment ID
    image_gen_url = f"{apim_gateway_url}/{inference_api_path}/openai/deployments/{model_name}/images/generations?api-version={image_api_version}"
    
    body = {
        "prompt": prompt,
        "size": size,
        "n": 1,
        "response_format": "b64_json"
    }
    try:
        r = requests.post(image_gen_url, headers=final_headers, json=body, timeout=120)
        if r.status_code != 200:
            print(f"[image] {model_name} failed: {r.status_code} {r.text[:300]}")
            return None
        data = r.json()
        images = data.get("data") or []
        if not images:
            print(f"[image] {model_name} returned no images.")
            return None
        b64 = images[0].get("b64_json")
        if not b64:
            print(f"[image] {model_name} missing b64_json field.")
            return None
        return b64
    except Exception as e:
        print(f"[image] Exception calling {model_name}: {e}")
        return None

# Vision chat endpoint (model-call style). We'll fallback to deployment style if 404.
VISION_CHAT_URL_MODEL = f"{apim_gateway_url}/{inference_api_path}/openai/chat/completions?api-version={image_api_version}"
VISION_CHAT_URL_DEPLOY = f"{apim_gateway_url}/{inference_api_path}/chat/completions?api-version={image_api_version}&deployment={vision_model}"  # legacy/deployment fallback

def analyze_image(b64_data: str, prompt: str) -> Optional[str]:
    if not b64_data:
        return None
    image_data_url = "data:image/png;base64," + b64_data
    messages = [
        {"role": "system", "content": "You are an expert vision analyst. Provide a concise description."},
        {"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_data_url}}
        ]}
    ]
    payload = {
        "model": vision_model,
        "messages": messages,
        "max_tokens": 300
    }
    # Try model style first
    try:
        r = requests.post(VISION_CHAT_URL_MODEL, headers=final_headers, json=payload, timeout=120)
        if r.status_code == 404:
            # Fallback to deployment-style path
            r = requests.post(VISION_CHAT_URL_DEPLOY, headers=final_headers, json=payload, timeout=120)
        if r.status_code != 200:
            print(f"[vision] Analysis failed: {r.status_code} {r.text[:300]}")
            return None
        resp = r.json()
        choices = resp.get("choices") or []
        if not choices:
            print("[vision] No choices returned.")
            return None
        vision_text = choices[0].get("message", {}).get("content")
        return vision_text
    except Exception as e:
        print(f"[vision] Exception analyzing image: {e}")
        return None

PROMPT = "A whimsical, futuristic workshop space where developers collaborate with friendly AI assistants; vibrant lighting, holographic interfaces, optimistic tone"

# Primary image attempt
primary_b64 = generate_image(image_model, PROMPT, DALL_E_DEFAULT_SIZE)
if primary_b64:
    print(f"[image] Primary image generated from '{image_model}' ({len(primary_b64)} base64 chars)")
else:
    print(f"[image] Primary image generation failed for '{image_model}'.")

# Optional FLUX second style if distinct and present
flux_b64 = None
if flux_model and flux_model != image_model:
    flux_b64 = generate_image(flux_model, PROMPT + " in cinematic style", FLUX_DEFAULT_SIZE)
    if flux_b64:
        print(f"[image] FLUX image generated from '{flux_model}' ({len(flux_b64)} base64 chars)")
    else:
        print("[image] FLUX generation failed or skipped.")
else:
    print("[image] FLUX not configured or same as primary.")

# Vision analysis
vision_summary = analyze_image(primary_b64, "Describe noteworthy visual details and overall style.") if primary_b64 else None
if vision_summary:
    print("[vision] Summary:\n" + vision_summary)
else:
    print("[vision] No vision summary produced.")

# Inline rendering (best-effort)
try:
    from IPython.display import display
    import matplotlib.pyplot as plt
    import io
    if primary_b64:
        import PIL.Image as Image
        img_bytes = base64.b64decode(primary_b64)
        im = Image.open(io.BytesIO(img_bytes))
        plt.figure(figsize=(4,4))
        plt.imshow(im)
        plt.axis('off')
        plt.title(f"Primary: {image_model}")
        display(plt.gcf())
    if flux_b64:
        import PIL.Image as Image
        img_bytes2 = base64.b64decode(flux_b64)
        im2 = Image.open(io.BytesIO(img_bytes2))
        plt.figure(figsize=(4,4))
        plt.imshow(im2)
        plt.axis('off')
        plt.title(f"FLUX: {flux_model}")
        display(plt.gcf())
except Exception as e:
    print(f"[display] Skipped inline rendering: {e}")

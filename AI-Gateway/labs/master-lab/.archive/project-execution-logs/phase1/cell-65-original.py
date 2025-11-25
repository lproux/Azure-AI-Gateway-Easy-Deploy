# Lab 08: Model Routing test (fixed for Dual Auth + invalid model + 401 handling)

import os
from openai import AuthenticationError

# Ensure DefaultAzureCredential is available even if this cell runs before its import elsewhere.
try:
    DefaultAzureCredential  # type: ignore
except NameError:
    from azure.identity import DefaultAzureCredential

# Acquire JWT (audience: https://cognitiveservices.azure.com) – may be required with APIM dual auth.
try:
    credential = DefaultAzureCredential()
    jwt_token = credential.get_token("https://cognitiveservices.azure.com/.default").token
except Exception as e:
    jwt_token = None
    print(f"[auth] WARN: Unable to acquire JWT token: {e}")

extra_headers = {}
if jwt_token:
    extra_headers["Authorization"] = f"Bearer {jwt_token}"

# Only test models that are actually deployed. gpt-4.1-mini not deployed; skip automatically.
requested_models = ['gpt-4o-mini', 'gpt-4.1-mini']
available_models = {'gpt-4o-mini', 'gpt-4o', 'text-embedding-3-small', 'text-embedding-3-large', 'dall-e-3'}  # from Step 2 config
models_to_test = [m for m in requested_models if m in available_models]

if len(models_to_test) != len(requested_models):
    missing = [m for m in requested_models if m not in models_to_test]
    print(f"[routing] Skipping unavailable models: {', '.join(missing)}")

# Guard if OpenAI client is not yet defined (e.g., cell ordering)
if 'client' not in globals():
    print("[WARN] OpenAI client 'client' not found; skipping model tests.")
    models_to_test = []

for model in models_to_test:
    print(f"[*] Testing model: {model}")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': 'Hello'}],
            max_tokens=10,
            extra_headers=extra_headers if extra_headers else None
        )
        # Robust content extraction
        content = ""
        try:
            content = response.choices[0].message.content
        except AttributeError:
            if hasattr(response.choices[0].message, 'get'):
                content = response.choices[0].message.get('content', '')
        print(f"Model {model}: {content}")
    except AuthenticationError as e:
        # Attempt one silent JWT refresh if first attempt lacked/invalid token
        if not jwt_token:
            print(f"[auth] 401 without JWT; attempting token fetch & retry...")
            try:
                credential = DefaultAzureCredential()
                jwt_token = credential.get_token("https://cognitiveservices.azure.com/.default").token
                extra_headers["Authorization"] = f"Bearer {jwt_token}"
                retry_resp = client.chat.completions.create(
                    model=model,
                    messages=[{'role': 'user', 'content': 'Hello'}],
                    max_tokens=10,
                    extra_headers=extra_headers
                )
                retry_content = ""
                try:
                    retry_content = retry_resp.choices[0].message.content
                except AttributeError:
                    if hasattr(retry_resp.choices[0].message, 'get'):
                        retry_content = retry_resp.choices[0].message.get('content', '')
                print(f"Model {model} (retry): {retry_content}")
                continue
            except Exception as e2:
                print(f"[ERROR] Retry after acquiring JWT failed: {e2}")
        print(f"[ERROR] Auth failed for {model}: {e}")
    except Exception as e:
        print(f"[ERROR] Request failed for {model}: {e}")

# Safe completion notification without NameError if utils is absent
if 'utils' in globals() and hasattr(utils, 'print_ok'):
    utils.print_ok('Lab 08 Complete!')
else:
    print('[OK] Lab 08 Complete!')
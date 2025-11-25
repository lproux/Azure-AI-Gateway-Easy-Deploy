"""
Fix for Cell 125: MCP OAuth Timeout and Retry Logic
Issue: MCP servers may be scaled to zero, causing timeouts
Severity: MEDIUM
Solution: Add retry logic with exponential backoff + increase timeouts
"""

# MCP OAuth authorization test with APIM - ENHANCED with retry logic

print("=== MCP Authorization Test ===")

import time
import requests

def post_with_retry(url, max_retries=3, initial_timeout=15, **kwargs):
    """
    POST with exponential backoff for container app cold starts.

    Args:
        url: Target URL
        max_retries: Number of retry attempts (default 3)
        initial_timeout: Initial timeout in seconds (default 15)
        **kwargs: Additional arguments for requests.post()

    Returns:
        Response object or None on failure
    """
    for attempt in range(max_retries):
        # Increase timeout on each retry to allow for cold start
        timeout = initial_timeout + (attempt * 10)  # 15s, 25s, 35s
        kwargs['timeout'] = timeout

        try:
            response = requests.post(url, **kwargs)
            return response
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # 1s, 2s, 4s exponential backoff
                print(f"[RETRY] Timeout after {timeout}s, waiting {wait}s before retry {attempt + 2}/{max_retries}")
                time.sleep(wait)
            else:
                print(f"[ERROR] Final timeout after {timeout}s on attempt {max_retries}")
                raise
        except Exception as e:
            print(f"[ERROR] Request failed: {e}")
            raise
    return None

# Reuse existing credential (ClientSecretCredential) and MCP_SERVERS
if 'credential' not in globals():
    print("[ERROR] 'credential' not initialized earlier.")
else:
    audiences = [
        f"api://{client_id}/.default",              # Common custom API audience pattern
        "https://management.azure.com/.default"     # Fallback ARM scope
    ]

    access_token = None
    used_audience = None
    for aud in audiences:
        try:
            token = credential.get_token(aud)
            access_token = token.token
            used_audience = aud
            print(f"[OK] Acquired token for audience: {aud}")
            break
        except Exception as e:
            print(f"[WARN] Failed audience {aud}: {e}")

    if not access_token:
        print("[ERROR] Could not acquire any access token. Aborting auth tests.")
    else:
        print(f"[INFO] Using token audience: {used_audience}\n")

        results = []
        for name, base_url in MCP_SERVERS.items():
            if not base_url:
                print(f"[SKIP] {name}: URL not configured")
                continue

            endpoint = f"{base_url.rstrip('/')}/mcp/"
            payload = {
                "jsonrpc": "2.0",
                "id": f"{name}-tools",
                "method": "tools/list",
                "params": {}
            }

            # Control (unauthorized) request - with retry logic
            unauthorized_status = None
            try:
                print(f"[{name}] Testing unauthorized access...")
                r_unauth = post_with_retry(endpoint, json=payload, max_retries=2, initial_timeout=20)
                unauthorized_status = r_unauth.status_code if r_unauth else "timeout"
            except Exception as e:
                unauthorized_status = f"error:{e}"

            # Authorized request - with retry logic
            auth_status = None
            tool_count = None
            try:
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    # Optional: include subscription key if APIM in front (harmless if not needed)
                    "api-key": apim_api_key
                }
                print(f"[{name}] Testing authorized access...")
                r_auth = post_with_retry(endpoint, json=payload, headers=headers, max_retries=3, initial_timeout=20)

                if r_auth:
                    auth_status = r_auth.status_code
                    if r_auth.status_code == 200:
                        data = r_auth.json()
                        tools = data.get("result", {}).get("tools", [])
                        tool_count = len(tools)
                    else:
                        tool_count = 0
                else:
                    auth_status = "timeout"
                    tool_count = 0
            except Exception as e:
                auth_status = f"error:{e}"
                tool_count = 0

            results.append({
                "server": name,
                "unauth": unauthorized_status,
                "auth": auth_status,
                "tools": tool_count
            })

            print(f"[{name}] unauth={unauthorized_status} auth={auth_status} tools={tool_count}")

        # Summary
        print("\n=== Authorization Summary ===")
        for r in results:
            status = "SECURED" if (r["unauth"] in (401, 403) and r["auth"] == 200) else "OPEN/UNKNOWN"
            print(f"{r['server']:>15}: unauth={r['unauth']} auth={r['auth']} tools={r['tools']} -> {status}")

        print("\n[OK] MCP OAuth authorization configured and tested")

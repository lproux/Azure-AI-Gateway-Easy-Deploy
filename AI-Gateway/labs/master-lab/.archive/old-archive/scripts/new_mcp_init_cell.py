# MCP Client Initialization (Clean Pattern - Based on Workshop)
# Run this cell BEFORE any MCP-dependent labs
print(" Initializing MCP Client...")
print("=" * 80)

from pathlib import Path
import httpx
import os

def _load_env_file(path: Path):
    """Load key=value pairs into environment and notebook scope."""
    if not path.exists():
        print(f" master-lab.env not found at {path}. Skipping auto-load.")
        return
    print(f" Loading environment variables from {path}...")
    protected_prefixes = ("APIM_", "AZURE_OPENAI_", "REDIS_", "COSMOS_", "SEARCH_", "CONTENT_SAFETY_")
    with path.open("r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ[key] = value
            globals()[key] = value
            if key.startswith(protected_prefixes):
                masked = value if len(value) <= 8 else f"{value[:4]}...{value[-4:]}"
                print(f"  {key} -> {masked}")
    print(" Environment variables loaded.\n")

# Load master-lab.env
_load_env_file(Path("master-lab.env"))

# Initialize MCP Client
config_path = Path('.mcp-servers-config')
if not config_path.exists():
    print(" ERROR: .mcp-servers-config file not found in working directory.")
    print(" Create this file with lines like: MCP_SERVER_WEATHER_URL=https://...")
    print(" Skipping MCP initialization.")
else:
    try:
        from notebook_mcp_helpers import MCPClient, MCPError
        mcp = MCPClient()
        print(" MCP client created successfully.")

        # Display configured servers
        print("\n MCP Servers Configuration:")
        print(f"  Weather: {mcp.weather.server_url[:60] if mcp.weather.server_url else 'NOT CONFIGURED'}{'...' if mcp.weather.server_url and len(mcp.weather.server_url) > 60 else ''}")
        print(f"  OnCall: {mcp.oncall.server_url[:60] if mcp.oncall.server_url else 'NOT CONFIGURED'}{'...' if mcp.oncall.server_url and len(mcp.oncall.server_url) > 60 else ''}")
        print(f"  GitHub: {mcp.github.server_url[:60] if mcp.github.server_url else 'NOT CONFIGURED'}{'...' if mcp.github.server_url and len(mcp.github.server_url) > 60 else ''}")
        print(f"  Spotify: {mcp.spotify.server_url[:60] if mcp.spotify.server_url else 'NOT CONFIGURED'}{'...' if mcp.spotify.server_url and len(mcp.spotify.server_url) > 60 else ''}")
        print(f"  Product Catalog: {mcp.product_catalog.server_url[:60] if mcp.product_catalog.server_url else 'NOT CONFIGURED'}{'...' if mcp.product_catalog.server_url and len(mcp.product_catalog.server_url) > 60 else ''}")
        print(f"  Place Order: {mcp.place_order.server_url[:60] if mcp.place_order.server_url else 'NOT CONFIGURED'}{'...' if mcp.place_order.server_url and len(mcp.place_order.server_url) > 60 else ''}")
        print(f"  MS Learn: {mcp.ms_learn.server_url[:60] if mcp.ms_learn.server_url else 'NOT CONFIGURED'}{'...' if mcp.ms_learn.server_url and len(mcp.ms_learn.server_url) > 60 else ''}")

        # Quick connectivity probe for one server
        def probe_server(name: str, url: str):
            """Quick probe to check if server is reachable"""
            if not url:
                print(f"\n  Skipping probe for {name} (no URL configured).")
                return
            print(f"\n Probing {name} server...")
            try:
                r = httpx.get(url.rstrip('/'), timeout=3.0)
                if r.status_code < 500:
                    print(f"  HTTP status: {r.status_code} (Server is reachable)")
                else:
                    print(f"  HTTP status: {r.status_code} (Server error)")
            except httpx.TimeoutException:
                print(f"  Timeout - Server not responding (may be starting up)")
            except Exception as http_err:
                print(f"  Connection warning: {type(http_err).__name__}")

        # Probe weather server as a quick test
        probe_server("Weather", mcp.weather.server_url)

        print("\n MCP initialization complete!")
        print("\n Note: If servers show timeouts, they may need to be restarted.")
        print(" Run test_mcp_servers.py for detailed server status.")

    except ImportError as e:
        print(f" ERROR: Failed to import MCP helpers: {e}")
        print(" Verify notebook_mcp_helpers.py is in the current directory.")
    except Exception as e:
        print(f" MCP initialization failed: {e}")
        print(" Verify .mcp-servers-config file format is KEY=VALUE per line.")

print("\n" + "=" * 80)

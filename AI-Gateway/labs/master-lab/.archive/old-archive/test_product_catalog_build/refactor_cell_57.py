#!/usr/bin/env python3
"""Refactor cell 57 to use WeatherMCP helper"""

import json

# Load notebook
with open('../master-ai-gateway.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# New cell content using WeatherMCP helper
new_cell_content = """# Lab 10 Example: Weather MCP Server
# Demonstrates weather data retrieval via MCP

# Approach 1: Using WeatherMCP helper from notebook_mcp_helpers.py
# This approach uses the working StreamableHTTPMCPClient pattern

from notebook_mcp_helpers import WeatherMCP

# Create Weather client with HTTP server URL
weather_server_url = "http://4.255.12.152:8080"
weather = WeatherMCP(weather_server_url)

print("[*] Connecting to weather MCP server...")
print(f"[*] Server URL: {weather_server_url}")

try:
    # Get list of cities for USA
    print()
    print("[*] Getting cities in USA...")
    cities_result = weather.get_cities("usa")
    print(f"[SUCCESS] Cities in USA: {cities_result}")

    # Get weather for Seattle
    print()
    print("[*] Getting weather for Seattle...")
    weather_result = weather.get_weather("Seattle")

    # Display result
    print('[SUCCESS] Weather data:')
    print('-' * 40)

    # Format output
    import json
    if isinstance(weather_result, str):
        # Parse string result
        import ast
        try:
            result_parsed = ast.literal_eval(weather_result)
            output = json.dumps(result_parsed, indent=2)
        except:
            output = weather_result
    else:
        output = json.dumps(weather_result, indent=2)

    # Truncate if too long
    if len(output) > 800:
        output = output[:800] + '\\n...\\n(truncated)'
    print(output)

    # Get weather for more cities
    print()
    print("[*] Getting weather for New York...")
    ny_weather = weather.get_weather("New York")
    print(f"[SUCCESS] New York weather: {ny_weather}")

except Exception as e:
    print(f"[ERROR] weather: {type(e).__name__}: {e}")
    print("[HINT] Server may be down or URL may be incorrect")

print()
print('[OK] Weather demo complete')
"""

# Update cell 57
nb['cells'][57]['source'] = new_cell_content.split('\n')

# Save notebook
with open('../master-ai-gateway.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Cell 57 refactored successfully!")
print("Updated to use WeatherMCP helper with Streamable HTTP transport")

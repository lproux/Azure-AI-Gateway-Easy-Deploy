#!/usr/bin/env python3
"""Refactor Spotify cells 61, 73, 75 to use SpotifyMCP helper"""

import json

# Load notebook
with open('../master-ai-gateway.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# New content for cell 61
cell_61_content = """# Lab 11: Spotify MCP Integration
# Demonstrates music service integration via MCP

# Approach 1: Using SpotifyMCP helper from notebook_mcp_helpers.py
# This approach uses the working StreamableHTTPMCPClient pattern

from notebook_mcp_helpers import SpotifyMCP

# Create Spotify client with HTTP server URL
spotify_server_url = "http://4.250.186.135:8080"
spotify = SpotifyMCP(spotify_server_url)

print("[*] Connecting to spotify MCP server...")
print(f"[*] Server URL: {spotify_server_url}")

try:
    # Search for jazz tracks
    print()
    print("[*] Searching for jazz tracks...")
    search_result = spotify.search("jazz", "track", 5)

    # Display result
    print('[SUCCESS] Search results:')
    print('-' * 40)

    # Format output
    import json
    if isinstance(search_result, str):
        import ast
        try:
            result_parsed = ast.literal_eval(search_result)
            output = json.dumps(result_parsed, indent=2)
        except:
            output = search_result
    else:
        output = json.dumps(search_result, indent=2)

    if len(output) > 800:
        output = output[:800] + '\\n...\\n(truncated)'
    print(output)

    # Get user playlists
    print()
    print("[*] Getting user playlists...")
    playlists = spotify.get_user_playlists(5)
    print(f"[SUCCESS] Playlists: {playlists}")

except Exception as e:
    print(f"[ERROR] spotify: {type(e).__name__}: {e}")
    print("[HINT] Server may be down or URL may be incorrect")

print()
print('[OK] Spotify demo complete')
"""

# New content for cell 73
cell_73_content = """# Spotify: Search for tracks

from notebook_mcp_helpers import SpotifyMCP

spotify_server_url = "http://4.250.186.135:8080"
spotify = SpotifyMCP(spotify_server_url)

print("[*] Searching for Miles Davis tracks...")

try:
    # Search for Miles Davis tracks
    results = spotify.search("Miles Davis", "track", 10)

    print('[SUCCESS] Search results:')
    print('-' * 40)

    # Format output
    import json
    if isinstance(results, str):
        import ast
        try:
            result_parsed = ast.literal_eval(results)
            output = json.dumps(result_parsed, indent=2)
        except:
            output = results
    else:
        output = json.dumps(results, indent=2)

    if len(output) > 1000:
        output = output[:1000] + '\\n...\\n(truncated)'
    print(output)

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")

print()
print('[OK] Spotify search complete')
"""

# New content for cell 75
cell_75_content = """# Spotify: Get playlists and tracks

from notebook_mcp_helpers import SpotifyMCP

spotify_server_url = "http://4.250.186.135:8080"
spotify = SpotifyMCP(spotify_server_url)

print("[*] Getting user playlists...")

try:
    # Get playlists
    playlists = spotify.get_user_playlists(10)

    print('[SUCCESS] User playlists:')
    print('-' * 40)

    # Format output
    import json
    if isinstance(playlists, str):
        import ast
        try:
            result_parsed = ast.literal_eval(playlists)
            output = json.dumps(result_parsed, indent=2)
        except:
            output = playlists
    else:
        output = json.dumps(playlists, indent=2)

    if len(output) > 800:
        output = output[:800] + '\\n...\\n(truncated)'
    print(output)

    # Get playlist tracks
    print()
    print("[*] Getting tracks from first playlist...")
    playlist_tracks = spotify.get_playlist_tracks("playlist1", 10)
    print(f"[SUCCESS] Playlist tracks: {playlist_tracks}")

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")

print()
print('[OK] Spotify playlists complete')
"""

# Update cells
nb['cells'][61]['source'] = cell_61_content.split('\n')
nb['cells'][73]['source'] = cell_73_content.split('\n')
nb['cells'][75]['source'] = cell_75_content.split('\n')

# Save notebook
with open('../master-ai-gateway.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Cells 61, 73, 75 refactored successfully!")
print("All Spotify cells updated to use SpotifyMCP helper with Streamable HTTP transport")

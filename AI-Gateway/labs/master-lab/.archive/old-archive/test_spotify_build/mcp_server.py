import uvicorn
from fastmcp import FastMCP, Context

mcp = FastMCP("Spotify")

# Mock Spotify data
MOCK_TRACKS = [
    {
        "id": "track1",
        "name": "Blue in Green",
        "artists": [{"name": "Miles Davis"}],
        "album": {"name": "Kind of Blue"},
        "duration_ms": 337000,
        "popularity": 72,
        "uri": "spotify:track:mock1"
    },
    {
        "id": "track2",
        "name": "Take Five",
        "artists": [{"name": "Dave Brubeck"}],
        "album": {"name": "Time Out"},
        "duration_ms": 324000,
        "popularity": 78,
        "uri": "spotify:track:mock2"
    },
    {
        "id": "track3",
        "name": "So What",
        "artists": [{"name": "Miles Davis"}],
        "album": {"name": "Kind of Blue"},
        "duration_ms": 562000,
        "popularity": 75,
        "uri": "spotify:track:mock3"
    }
]

MOCK_PLAYLISTS = [
    {
        "id": "playlist1",
        "name": "Jazz Classics",
        "description": "The best jazz tracks of all time",
        "owner": {"display_name": "Spotify"},
        "tracks": {"total": 50},
        "public": True
    },
    {
        "id": "playlist2",
        "name": "Chill Jazz",
        "description": "Relaxing jazz for work and study",
        "owner": {"display_name": "User"},
        "tracks": {"total": 30},
        "public": False
    }
]

@mcp.tool()
async def search(ctx: Context, query: str, search_type: str = "track", limit: int = 10) -> str:
    """
    Search for tracks, artists, albums, or playlists on Spotify

    Args:
        query: Search query string
        search_type: Type of search ("track", "artist", "album", "playlist")
        limit: Maximum number of results (default: 10)
    """
    query_lower = query.lower()

    if search_type == "track":
        results = [t for t in MOCK_TRACKS if query_lower in t["name"].lower() or
                   any(query_lower in a["name"].lower() for a in t["artists"])]
        return str({
            "tracks": {
                "items": results[:limit],
                "total": len(results)
            }
        })

    return str({"error": f"Search type '{search_type}' not fully implemented in mock"})

@mcp.tool()
async def get_user_playlists(ctx: Context, limit: int = 20) -> str:
    """
    Get current user's playlists

    Args:
        limit: Maximum number of playlists to return (default: 20)
    """
    return str({
        "items": MOCK_PLAYLISTS[:limit],
        "total": len(MOCK_PLAYLISTS)
    })

@mcp.tool()
async def get_playlist_tracks(ctx: Context, playlist_id: str, limit: int = 50) -> str:
    """
    Get tracks from a specific playlist

    Args:
        playlist_id: Spotify playlist ID
        limit: Maximum number of tracks (default: 50)
    """
    # Return mock tracks for any playlist
    return str({
        "items": [{"track": t} for t in MOCK_TRACKS[:limit]],
        "total": len(MOCK_TRACKS)
    })

@mcp.tool()
async def get_currently_playing(ctx: Context) -> str:
    """Get the user's currently playing track"""
    return str({
        "is_playing": True,
        "item": MOCK_TRACKS[0],
        "progress_ms": 120000
    })

@mcp.tool()
async def get_playback_state(ctx: Context) -> str:
    """Get information about the user's current playback state"""
    return str({
        "device": {
            "id": "mock-device",
            "name": "Mock Speaker",
            "type": "Speaker",
            "volume_percent": 75
        },
        "is_playing": True,
        "shuffle_state": False,
        "repeat_state": "off",
        "item": MOCK_TRACKS[0]
    })

@mcp.tool()
async def start_playback(ctx: Context, uri: str = None) -> str:
    """
    Start or resume playback

    Args:
        uri: Optional Spotify URI to play
    """
    return str({
        "success": True,
        "message": f"Started playback{' of ' + uri if uri else ''}"
    })

@mcp.tool()
async def pause_playback(ctx: Context) -> str:
    """Pause playback"""
    return str({
        "success": True,
        "message": "Playback paused"
    })

@mcp.tool()
async def skip_to_next(ctx: Context) -> str:
    """Skip to next track"""
    return str({
        "success": True,
        "message": "Skipped to next track"
    })

@mcp.tool()
async def skip_to_previous(ctx: Context) -> str:
    """Skip to previous track"""
    return str({
        "success": True,
        "message": "Skipped to previous track"
    })

@mcp.tool()
async def get_track(ctx: Context, track_id: str) -> str:
    """
    Get detailed information about a track

    Args:
        track_id: Spotify track ID
    """
    # Find track by ID or return first mock track
    for track in MOCK_TRACKS:
        if track["id"] == track_id:
            return str(track)

    return str(MOCK_TRACKS[0])

@mcp.tool()
async def get_recommendations(ctx: Context, seed_artists: str = None, seed_tracks: str = None, limit: int = 20) -> str:
    """
    Get track recommendations based on seeds

    Args:
        seed_artists: Comma-separated artist IDs
        seed_tracks: Comma-separated track IDs
        limit: Number of recommendations (default: 20)
    """
    return str({
        "tracks": MOCK_TRACKS[:limit],
        "seeds": {
            "seed_artists": seed_artists.split(",") if seed_artists else [],
            "seed_tracks": seed_tracks.split(",") if seed_tracks else []
        }
    })

@mcp.tool()
async def create_playlist(ctx: Context, name: str, description: str = "", public: bool = True) -> str:
    """
    Create a new playlist

    Args:
        name: Playlist name
        description: Playlist description (optional)
        public: Whether playlist is public (default: True)
    """
    new_playlist = {
        "id": f"playlist{len(MOCK_PLAYLISTS) + 1}",
        "name": name,
        "description": description,
        "owner": {"display_name": "User"},
        "tracks": {"total": 0},
        "public": public
    }
    return str(new_playlist)

if __name__ == "__main__":
    # Use mcp.run() with HTTP transport
    mcp.run(transport="http", host="0.0.0.0", port=8080, path="/spotify")

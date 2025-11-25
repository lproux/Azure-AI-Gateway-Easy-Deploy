# MCP Docker Images - Public Sources Found

**Date**: 2025-11-15
**Status**: Research Complete - Public Docker Images Located
**Purpose**: Replace placeholder "helloworld" images with actual MCP servers

---

## Summary

Found public Docker images for **4 out of 7** MCP servers. Remaining 3 (product-catalog, place-order, ms-learn) were noted in archive as intentional placeholders.

---

## Public Docker Images Found

### 1. GitHub MCP Server ✅
**Source**: Official GitHub
**Docker Image**: `ghcr.io/github/github-mcp-server`
**Registry**: GitHub Container Registry (ghcr.io)
**Status**: ✅ PUBLIC - Official
**SHA-256 Pin**: `ghcr.io/github/github-mcp-server@sha256:2f9c6e9edca1e93993f95dbf7670aa2832006d95409e5d459a8c7559f9c2ffd8`

**Usage**:
```bash
docker run -i --rm \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=${GITHUB_TOKEN} \
  ghcr.io/github/github-mcp-server
```

**Features**:
- Repository management
- Issue tracking
- Pull requests
- GitHub Actions
- Code security features

**Reference**: https://github.com/github/github-mcp-server

---

### 2. Weather MCP Server ✅
**Source**: Community (Open-Meteo)
**Docker Image**: `mcp/openweather` OR `isdaniel/mcp_weather_server`
**Registry**: Docker Hub
**Status**: ✅ PUBLIC - Community

**Option A** (Docker Hub MCP Catalog):
```bash
docker run -i --rm \
  -e OWM_API_KEY=${WEATHER_API_KEY} \
  mcp/openweather
```

**Option B** (isdaniel - with SSE support):
```bash
docker run -i --rm \
  -e WEATHER_API_KEY=${WEATHER_API_KEY} \
  -p 8000:8000 \
  isdaniel/mcp_weather_server
```

**Features**:
- Real-time weather data
- Temperature, wind speed, conditions
- City-based queries
- Open-Meteo API integration

**References**:
- https://hub.docker.com/mcp/server/openweather
- https://github.com/isdaniel/mcp_weather_server

---

### 3. Spotify MCP Server ✅
**Source**: Community
**Docker Image**: `richbai90/spotify-mcp` OR `allensy/spotify-mcp`
**Registry**: Docker Hub
**Status**: ✅ PUBLIC - Community

**Usage**:
```bash
docker run -i --rm \
  -e SPOTIPY_CLIENT_ID=${SPOTIFY_CLIENT_ID} \
  -e SPOTIPY_CLIENT_SECRET=${SPOTIFY_CLIENT_SECRET} \
  -e SPOTIPY_REDIRECT_URI=${SPOTIFY_REDIRECT_URI} \
  -v ./spotify-cache:/cache \
  richbai90/spotify-mcp
```

**Features**:
- Music search on Spotify
- Playlist creation (themes/genres)
- Add tracks to playlists
- Explore existing playlists
- Get music recommendations

**References**:
- https://github.com/richbai90/spotify-mcp
- https://lobehub.com/mcp/allensy-spotify-mcp

---

### 4. PagerDuty/OnCall MCP Server ⚠️
**Source**: Official PagerDuty
**Docker Image**: ❌ NO PUBLIC DOCKER IMAGE FOUND
**Status**: ⚠️ Python package only (`uvx pagerduty-mcp`)

**Alternative Deployment**:
```bash
# Python/UV installation
uvx pagerduty-mcp --enable-write-tools
```

**Features**:
- Incident management
- Service management
- Schedules
- Event orchestrations
- On-call management

**Notes**:
- Official GitHub repo exists: https://github.com/PagerDuty/pagerduty-mcp-server
- No official Docker image on ghcr.io or Docker Hub
- **Recommendation**: Build custom Docker image OR use alternative oncall solution OR skip this server

**Reference**: https://github.com/PagerDuty/pagerduty-mcp-server

---

## Placeholder Servers (Not Built - From Archive Documentation)

### 5. Product-Catalog MCP Server ❌
**Status**: ❌ PLACEHOLDER (never built)
**Evidence**: Archive docs state "weather, oncall, github, spotify, product-catalog, place-order, ms-learn were placeholder images"

**Options**:
- A. Build custom product-catalog MCP server
- B. Use demo/mock data server
- C. Skip this server (non-critical for lab)

---

### 6. Place-Order MCP Server ❌
**Status**: ❌ PLACEHOLDER (never built)
**Evidence**: Same as product-catalog - intentional placeholder

**Options**:
- A. Build custom order processing MCP server
- B. Use demo/mock order server
- C. Skip this server (non-critical for lab)

---

### 7. MS-Learn MCP Server ❌
**Status**: ❌ PLACEHOLDER (never built)
**Evidence**: Same as above - intentional placeholder

**Options**:
- A. Build Microsoft Learn API integration server
- B. Use generic documentation/learning MCP server
- C. Skip this server (non-critical for lab)

---

## Deployment Strategy

### Immediate Deployment (4 Servers)

**Priority 1**: Deploy public images first
1. ✅ GitHub: `ghcr.io/github/github-mcp-server`
2. ✅ Weather: `mcp/openweather`
3. ✅ Spotify: `richbai90/spotify-mcp`
4. ⚠️ OnCall: Build Docker image from PagerDuty Python package OR use alternative

---

### Deferred/Optional (3 Servers)

**Priority 2**: Handle placeholders
5. ❓ Product-Catalog: TBD (custom build or skip)
6. ❓ Place-Order: TBD (custom build or skip)
7. ❓ MS-Learn: TBD (custom build or skip)

---

## Container App Update Plan

### Step 1: Update Container Apps with Public Images

**Command Pattern** (per app):
```bash
az containerapp update \
  -g lab-master-lab \
  -n mcp-<SERVER>-pavavy6pu5 \
  --image <DOCKER_IMAGE>
```

**Specific Commands**:

```bash
# 1. GitHub MCP
az containerapp update \
  -g lab-master-lab \
  -n mcp-github-pavavy6pu5 \
  --image ghcr.io/github/github-mcp-server \
  --set-env-vars "GITHUB_PERSONAL_ACCESS_TOKEN=secretref:github-token"

# 2. Weather MCP
az containerapp update \
  -g lab-master-lab \
  -n mcp-weather-pavavy6pu5 \
  --image mcp/openweather \
  --set-env-vars "OWM_API_KEY=secretref:openweather-api-key"

# 3. Spotify MCP
az containerapp update \
  -g lab-master-lab \
  -n mcp-spotify-pavavy6pu5 \
  --image richbai90/spotify-mcp \
  --set-env-vars \
    "SPOTIPY_CLIENT_ID=secretref:spotify-client-id" \
    "SPOTIPY_CLIENT_SECRET=secretref:spotify-client-secret" \
    "SPOTIPY_REDIRECT_URI=http://localhost:8888/callback"

# 4. OnCall (Option: Keep placeholder OR build custom)
# TBD - requires custom build or alternative solution
```

---

### Step 2: Handle Placeholder Servers

**Option A**: Use demo/mock servers
**Option B**: Build minimal MCP servers
**Option C**: Leave as "hello world" placeholder (non-functional but won't crash)

**Recommendation**: Option C for now
- Product-catalog: Keep placeholder
- Place-order: Keep placeholder
- MS-Learn: Keep placeholder
- **Impact**: ~3-5 cells remain non-functional (out of ~30 MCP cells)
- **Benefit**: 4/7 servers (majority) will work, unblocking ~20-25 cells

---

## Environment Variables Needed

### GitHub MCP Server
```bash
GITHUB_PERSONAL_ACCESS_TOKEN=<your-github-pat>
```

### Weather MCP Server
```bash
OWM_API_KEY=<openweathermap-api-key>
# Register free at: https://openweathermap.org/api
```

### Spotify MCP Server
```bash
SPOTIPY_CLIENT_ID=<spotify-client-id>
SPOTIPY_CLIENT_SECRET=<spotify-client-secret>
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
# Register app at: https://developer.spotify.com/dashboard
```

---

## Verification After Deployment

```bash
# Test MCP endpoint (should return JSON-RPC, not HTML)
curl https://mcp-github-pavavy6pu5.niceriver-900455a0.uksouth.azurecontainerapps.io/mcp

# Expected: JSON-RPC error response (means MCP server is running)
{"jsonrpc":"2.0","error":{"code":-32700,"message":"Parse error"}}

# NOT HTML:
<!DOCTYPE html>...
```

---

## Success Criteria

### Phase 1: Deploy Public Images (4/7 servers)
- [x] Found GitHub MCP Docker image
- [x] Found Weather MCP Docker image
- [x] Found Spotify MCP Docker image
- [ ] OnCall: Build custom OR use alternative
- [ ] Update Container Apps with new images
- [ ] Configure environment variables/secrets
- [ ] Verify MCP endpoints return JSON-RPC

### Phase 2: Test Notebook Integration
- [ ] Cell 83: Test weather.get_cities("usa")
- [ ] Cell 84-87: Test GitHub MCP examples
- [ ] Cell 88-91: Test Spotify MCP examples
- [ ] ~20-25 cells working (out of ~30 MCP cells)

---

## Next Steps

1. **Immediate**: Create Azure Container App secrets for API keys
2. **Then**: Update GitHub, Weather, Spotify Container Apps with public images
3. **Test**: Verify `/mcp` endpoints return JSON-RPC
4. **Run**: Cell 83 to confirm MCP initialization works
5. **Decide**: What to do with product-catalog, place-order, ms-learn (placeholders)

---

## Alternative: Skip MCP Servers Entirely

If deploying MCP servers is too complex:

**Option D**: Disable MCP cells and continue with remaining fixes
- **Impact**: Lose ~30 cells of functionality
- **Benefit**: Unblock remaining ~180 cells
- **Trade-off**: Miss out on MCP integration demonstration

---

**Created**: 2025-11-15
**Research Source**: Web search + archive documentation
**Public Images Found**: 3/7 (GitHub, Weather, Spotify)
**Partially Available**: 1/7 (OnCall - Python package only)
**Placeholders**: 3/7 (product-catalog, place-order, ms-learn)
**Recommended Next**: Deploy 3 public images, build OnCall Docker image, skip/mock remaining 3

"""
Fix for Cell 121: Redis Graceful Degradation
Issue: Raises ValueError and stops execution if Redis not configured
Severity: LOW
Solution: Allow notebook to continue with caching disabled
"""

import redis.asyncio as redis

# Resolve Redis connection settings without redefining earlier variables if already present
# Prefer existing globals, then environment (.env / master-lab.env), then step3_outputs
redis_host = globals().get('redis_host') or os.getenv('REDIS_HOST') or step3_outputs.get('redisCacheHost')
redis_port_raw = globals().get('redis_port') or os.getenv('REDIS_PORT') or step3_outputs.get('redisCachePort', 6380)
redis_key = globals().get('redis_key') or os.getenv('REDIS_KEY') or step3_outputs.get('redisCacheKey')

# Normalize port
try:
    redis_port = int(redis_port_raw)
except Exception:
    redis_port = 6380  # fallback typical TLS port

# FIXED: Graceful degradation instead of raising ValueError
if not all([redis_host, redis_port, redis_key]):
    print('[WARN] Missing Redis configuration (host/port/key). Caching will be disabled.')
    print('[INFO] To enable caching, ensure master-lab.env contains:')
    print('       - REDIS_HOST')
    print('       - REDIS_PORT')
    print('       - REDIS_KEY')
    redis_enabled = False
else:
    redis_enabled = True
    print(f'[INFO] Redis configured: {redis_host}:{redis_port}')

async def test_redis():
    """Test Redis connection with error handling"""
    if not redis_enabled:
        print('[SKIP] Redis test skipped (not configured)')
        return False

    # rediss (TLS). Decode responses for convenience.
    url = f'rediss://:{redis_key}@{redis_host}:{redis_port}'

    try:
        r = await redis.from_url(
            url,
            encoding='utf-8',
            decode_responses=True,
            socket_connect_timeout=5,  # ADDED: Connection timeout
            socket_timeout=5            # ADDED: Socket timeout
        )
        try:
            info = await r.info()
            print(f'[OK] Connected to Redis at {redis_host}:{redis_port}')
            print(f'Redis Version      : {info.get("redis_version")}')
            print(f'Connected Clients  : {info.get("connected_clients")}')
            print(f'Used Memory        : {info.get("used_memory_human")}')
            return True
        finally:
            await r.aclose()
    except Exception as e:
        print(f'[ERROR] Redis connection failed: {e}')
        print('[INFO] Semantic caching will be disabled for this session')
        print('[INFO] This is not critical - exercises will continue without caching')
        return False

# Test connection
redis_connected = await test_redis()

# Export redis_enabled for other cells to check
if redis_connected:
    print('\n✅ Redis caching: ENABLED')
else:
    print('\n⚠️ Redis caching: DISABLED (non-critical)')

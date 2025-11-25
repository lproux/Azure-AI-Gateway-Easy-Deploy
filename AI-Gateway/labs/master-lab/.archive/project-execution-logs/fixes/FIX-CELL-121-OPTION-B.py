# Cell 121 Fix - Option B: Add Connection Timeout

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

if not all([redis_host, redis_port, redis_key]):
    raise ValueError('Missing Redis configuration (host/port/key). Ensure master-lab.env is generated and loaded.')

async def test_redis():
    # rediss (TLS). Decode responses for convenience.
    url = f'rediss://:{redis_key}@{redis_host}:{redis_port}'
    # OPTION B: Add socket_connect_timeout and socket_timeout parameters
    r = await redis.from_url(
        url,
        encoding='utf-8',
        decode_responses=True,
        socket_connect_timeout=5,  # 5 second connection timeout
        socket_timeout=5            # 5 second socket timeout
    )
    try:
        info = await r.info()
        print(f'[OK] Connected to Redis at {redis_host}:{redis_port}')
        print(f'Redis Version      : {info.get("redis_version")}')
        print(f'Connected Clients  : {info.get("connected_clients")}')
        print(f'Used Memory        : {info.get("used_memory_human")}')
    finally:
        await r.aclose()

await test_redis()

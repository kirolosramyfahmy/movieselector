import json
from typing import Optional, Any
from app.core.redis import get_redis
from app.core.config import get_settings

settings = get_settings()


async def get_cached(key: str) -> Optional[Any]:
    """Get value from cache."""
    try:
        redis = await get_redis()
        value = await redis.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        print(f"Cache get error: {e}")
        return None


async def set_cached(key: str, value: Any, ttl: int = None) -> bool:
    """Set value in cache with optional TTL."""
    try:
        redis = await get_redis()
        if ttl is None:
            ttl = settings.cache_ttl_seconds
        
        await redis.setex(
            key,
            ttl,
            json.dumps(value)
        )
        return True
    except Exception as e:
        print(f"Cache set error: {e}")
        return False


async def delete_cached(key: str) -> bool:
    """Delete value from cache."""
    try:
        redis = await get_redis()
        await redis.delete(key)
        return True
    except Exception as e:
        print(f"Cache delete error: {e}")
        return False


async def clear_cache_pattern(pattern: str) -> int:
    """Clear all cache keys matching pattern."""
    try:
        redis = await get_redis()
        keys = await redis.keys(pattern)
        if keys:
            return await redis.delete(*keys)
        return 0
    except Exception as e:
        print(f"Cache clear error: {e}")
        return 0

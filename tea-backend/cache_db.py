import time
from typing import Any, Dict, Tuple, Callable, Awaitable

CACHE_TTL_SECONDS = 60

_cache: Dict[str, Tuple[Any, float]] = {}

def _is_expired(timestamp: float) -> bool:
    return (time.time() - timestamp) > CACHE_TTL_SECONDS

async def get_or_set_cache(key: str, fetch_func: Callable[[], Awaitable[Any]]) -> Any:
    if key in _cache:
        data, timestamp = _cache[key]
        if not _is_expired(timestamp):
            print(f"[CACHE HIT] key={key}")
            return data
        else:
            print(f"[CACHE EXPIRED] key={key}")
            del _cache[key]

    print(f"[CACHE MISS] key={key}")
    data = await fetch_func()
    _cache[key] = (data, time.time())
    return data

def invalidate_cache(key: str):
    _cache.pop(key, None)

def clear_cache_startswith(prefix: str):
    """Useful to invalidate groups like all post-related cache."""
    keys_to_delete = [k for k in _cache if k.startswith(prefix)]
    for k in keys_to_delete:
        _cache.pop(k, None)

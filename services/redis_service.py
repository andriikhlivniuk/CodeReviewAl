import redis

# Initialize Redis connection
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True  # Ensure responses are strings
)

def cache_set(key, value, ttl=3600):
    """
    Cache a key-value pair with an optional TTL (default: 1 hour).
    """
    redis_client.set(key, value, ex=ttl)

def cache_get(key):
    """
    Retrieve a value from the cache by key.
    """
    return redis_client.get(key)

def cache_delete(key):
    """
    Delete a key from the cache.
    """
    redis_client.delete(key)

import hashlib
import json
from flask import request
from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': 6379,
})

def make_cache_key(*args, **kwargs):
    request_data = request.get_json()
    key = json.dumps(request_data, sort_keys=True)
    return hashlib.md5(key.encode('utf-8')).hexdigest()

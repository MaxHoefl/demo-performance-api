from cachetools import Cache
from redis import Redis

from app.config import acquire_app_config


class RedisLruCache(Cache):
    def __init__(self, maxsize: int, getsizeof=None, redis=None):
        Cache.__init__(self, maxsize=maxsize, getsizeof=getsizeof)
        if redis:
            self.redis = redis
        else:
            config = acquire_app_config()
            self.redis = Redis.from_url(config.redis_url, charset="utf-8", decode_responses=True)
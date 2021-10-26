import redis

class RedisClient():
    def __init__(self, host, port, password):
        # 初始化数据库链接
        pool = redis.ConnectionPool(host=host, port=port, password=password)
        self._r = redis.Redis(connection_pool=pool)
    
    def handle_redis_token(self, key, value, expiration=300):
        self._r.setex(name=key, time=expiration, value=value)
    
    def close(self):
        self._r.close()
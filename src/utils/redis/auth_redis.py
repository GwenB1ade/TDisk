from redis import Redis

class AuthRedis:
    
    def __init__(self, redis: Redis):
        self.redis = redis
    
    
    def save_token(self, name: str, token: str):
        self.redis.set(name = name, value = token)
    
    
    def get_token(self, name: str):
        try:
            token = self.redis.get(name)
            return token
        except Exception as e:
            return e
    
    
    def delete_token(self, name: str):
        self.redis.delete(name)
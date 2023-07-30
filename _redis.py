import redis
import os

# Create a redis client

redisClient = redis.StrictRedis(
    host=os.getenv('REDIS_HOST'),
    username=os.getenv('REDIS_USERNAME'),
    password=os.getenv('REDIS_PASSWORD'),
    port=os.getenv('REDIS_PORT'),
    db=os.getenv('REDIS_DB'),
)

key = 'messages'

def push(message):
    redisClient.lpush(key, message)

def pop():
    return redisClient.blpop(key, 0)

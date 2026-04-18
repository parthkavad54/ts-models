import redis
import os
import json
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

CACHE_TTL = 3600  # 1 hour

def get_cached_risk_score(student_id: str):
    key = f"risk_score:{student_id}"
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
    except redis.exceptions.ConnectionError:
        print("Redis is offline. Bypassing cache.")
    return None

def set_cached_risk_score(student_id: str, data: dict):
    key = f"risk_score:{student_id}"
    try:
        redis_client.setex(key, CACHE_TTL, json.dumps(data))
    except redis.exceptions.ConnectionError:
        pass

def invalidate_cache(student_id: str):
    key = f"risk_score:{student_id}"
    try:
        redis_client.delete(key)
    except redis.exceptions.ConnectionError:
        pass

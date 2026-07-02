import json
import logging
from typing import Any, Optional
import redis
from app.core.config import settings

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self) -> None:
        self.client: Optional[redis.Redis] = None
        try:
            self.client = redis.from_url(settings.redis_uri, decode_responses=True)
            self.client.ping()
            logger.info("Successfully connected to Redis.")
        except Exception as e:
            logger.error(f"Could not connect to Redis: {e}")
            self.client = None

    def get(self, key: str) -> Optional[Any]:
        if not self.client:
            return None
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logger.error(f"Redis get failed for key '{key}': {e}")
        return None

    def set(self, key: str, value: Any, expire_seconds: int = 300) -> bool:
        if not self.client:
            return False
        try:
            serialized_data = json.dumps(value)
            self.client.set(key, serialized_data, ex=expire_seconds)
            return True
        except Exception as e:
            logger.error(f"Redis set failed for key '{key}': {e}")
            return False

    def delete(self, key: str) -> bool:
        if not self.client:
            return False
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis delete failed for key '{key}': {e}")
            return False

    def clear_pattern(self, pattern: str) -> bool:
        if not self.client:
            return False
        try:
            keys = self.client.keys(pattern)
            if keys:
                self.client.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"Redis clear pattern failed for '{pattern}': {e}")
            return False

    def ping(self) -> bool:
        if not self.client:
            return False
        try:
            return self.client.ping()
        except Exception:
            return False

cache_service = CacheService()

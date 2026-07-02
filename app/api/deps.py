from typing import Generator
from sqlalchemy.orm import Session
from app.database.session import get_db as db_generator
from app.services.cache import cache_service, CacheService

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get DB session per request.
    """
    yield from db_generator()

def get_cache() -> CacheService:
    """
    Dependency to get the Redis cache client service.
    """
    return cache_service

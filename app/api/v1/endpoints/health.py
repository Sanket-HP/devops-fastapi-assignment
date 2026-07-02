import time
import logging
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api.deps import get_db, get_cache
from app.services.cache import CacheService

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("", status_code=status.HTTP_200_OK)
def check_health(
    response: Response,
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache),
) -> dict:
    db_ok = False
    redis_ok = False
    
    # Check Database connection
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception as e:
        logger.error(f"Health check: Database connection failed: {e}")

    # Check Redis connection
    try:
        redis_ok = cache.ping()
        if not redis_ok:
            logger.error("Health check: Redis ping returned False")
    except Exception as e:
        logger.error(f"Health check: Redis connection failed: {e}")

    overall_status = "healthy"
    if not db_ok or not redis_ok:
        overall_status = "degraded" if (db_ok or redis_ok) else "unhealthy"
        # Return 503 Service Unavailable if database is down
        if not db_ok:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": overall_status,
        "timestamp": time.time(),
        "services": {
            "database": "healthy" if db_ok else "unhealthy",
            "redis": "healthy" if redis_ok else "unhealthy",
        }
    }

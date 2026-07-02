import time
from datetime import datetime
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
    timestamp = datetime.utcnow().isoformat()
    
    # Check Database connection & latency
    db_status = "connected"
    db_error = None
    db_latency = 0.0
    try:
        start_time = time.time()
        db.execute(text("SELECT 1"))
        db_latency = round((time.time() - start_time) * 1000, 2)
    except Exception as e:
        db_status = "disconnected"
        db_error = str(e)
        logger.error(f"Health check: Database connection failed: {e}")

    # Check Redis connection & latency
    redis_status = "connected"
    redis_error = None
    redis_latency = 0.0
    try:
        start_time = time.time()
        ping_ok = cache.ping()
        redis_latency = round((time.time() - start_time) * 1000, 2)
        if not ping_ok:
            redis_status = "disconnected"
            redis_error = "Redis ping returned False"
    except Exception as e:
        redis_status = "disconnected"
        redis_error = str(e)
        logger.error(f"Health check: Redis connection failed: {e}")

    # Determine overall status
    overall_status = "healthy"
    if db_status == "disconnected" or redis_status == "disconnected":
        overall_status = "degraded"
        # Return 503 Service Unavailable if database is down
        if db_status == "disconnected":
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    checks = {}
    if db_status == "connected":
        checks["database"] = {
            "status": "connected",
            "latency_ms": db_latency
        }
    else:
        checks["database"] = {
            "status": "disconnected",
            "error": db_error or "Unknown database error"
        }

    if redis_status == "connected":
        checks["redis"] = {
            "status": "connected",
            "latency_ms": redis_latency
        }
    else:
        checks["redis"] = {
            "status": "disconnected",
            "error": redis_error or "Unknown cache error"
        }

    return {
        "status": overall_status,
        "timestamp": timestamp,
        "checks": checks
    }

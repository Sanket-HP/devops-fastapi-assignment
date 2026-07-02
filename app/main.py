from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router
from app.database.base import Base
from app.database.session import engine

# Setup initial logs to capture startup events
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    logger.info("Starting up FastAPI application...")
    try:
        # Create database tables if they do not exist
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified/created.")
    except Exception as e:
        logger.critical(f"Database initialization failed on startup: {e}")
        raise e
        
    yield
    
    # Shutdown tasks
    logger.info("Shutting down FastAPI application...")

app = FastAPI(
    title=settings.APP_NAME,
    description="Production-ready FastAPI backend.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes. Included without /api/v1 prefix to expose /users and /health directly at root.
app.include_router(api_router)

@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    """
    Root endpoint returning service identification details.
    """
    return {
        "app": settings.APP_NAME,
        "environment": settings.ENV,
        "status": "online",
        "docs": "/docs"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global unhandled exception logger and response formatter.
    """
    logger.error(f"Unhandled exception for {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Please contact the administrator."}
    )

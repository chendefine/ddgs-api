import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.ddgs import cleanup_ddgs, initialize_ddgs
from app.mcp import mcp_app
from app.routes import search


# Filter to exclude health check and docs endpoints from access logs
class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        return not any(path in message for path in ["/healthz", "/docs", "/redoc", "/openapi.json"])


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """Application lifecycle management"""

    # Initialize DDGS on startup
    initialize_ddgs()

    # Add filter to uvicorn access logger to exclude /healthz logs
    logging.getLogger("uvicorn.access").addFilter(HealthCheckFilter())

    yield
    # Cleanup resources on shutdown (DDGS has no explicit close method, Python GC handles cleanup automatically)
    cleanup_ddgs()


# Combine both lifespans
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run both lifespans
    async with app_lifespan(app):
        async with mcp_app.lifespan(app):
            yield


app = FastAPI(
    title="DDGS API",
    description="DDGS API Service",
    version="0.1.0",
    lifespan=lifespan,
    docs_url=f"{settings.api_prefix}/docs",
    redoc_url=f"{settings.api_prefix}/redoc",
    openapi_url=f"{settings.api_prefix}/openapi.json",
)


# add health check
@app.get("/healthz")
async def health_check():
    return "DDGS API is running"


# Register routes
app.include_router(search.router, prefix=settings.api_prefix)

# add mcp server
app.mount(settings.api_prefix, mcp_app)

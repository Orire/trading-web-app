"""
FastAPI Main Application
Trading web interface backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from contextlib import asynccontextmanager
import logging

from app.api import signals, positions, markets, performance, advice, strategy
from app.settings import get_settings
from app.websocket.trading import setup_websocket

settings = get_settings()
logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)

# Create Socket.IO server
sio = socketio.AsyncServer(
    cors_allowed_origins=settings.cors_origin_list(),
    async_mode="asgi",
)
socket_app = socketio.ASGIApp(sio)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting application...")
    setup_websocket(sio)
    yield
    logger.info("Shutting down application...")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Backend API for trading web interface",
    version=settings.app_version,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(signals.router, prefix="/api/signals", tags=["signals"])
app.include_router(positions.router, prefix="/api/positions", tags=["positions"])
app.include_router(markets.router, prefix="/api/markets", tags=["markets"])
app.include_router(performance.router, prefix="/api/performance", tags=["performance"])
app.include_router(advice.router, prefix="/api/advice", tags=["advice"])
app.include_router(strategy.router, prefix="/api/strategy", tags=["strategy"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": settings.app_name, "version": settings.app_version}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

# Mount Socket.IO app
app.mount("/socket.io", socket_app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port)

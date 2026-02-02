"""
ADHD Coach Backend - Main Application

FastAPI application entry point for the ADHD coaching system.
"""

from fastapi import FastAPI
from datetime import datetime

from app.routers import auth, telegram, projects, patterns, admin

# Create FastAPI app instance
app = FastAPI(
    title="ADHD Coach API",
    description="Backend API for the ADHD coaching and work management system",
    version="0.1.0",
)

# CORS removed - no web frontend, Telegram only

# Include routers
app.include_router(auth.router)
app.include_router(telegram.router)
app.include_router(projects.router)
app.include_router(patterns.router)  # Pattern learning API
app.include_router(admin.router)  # Admin endpoints


# Initialize Telegram bot on startup
# DISABLED: Bot runs separately via run_telegram_bot.py
# @app.on_event("startup")
# async def startup_event():
#     """Initialize services on startup."""
#     print("🚀 Starting up...")
#     try:
#         from app.services.telegram_service import get_telegram_service
#         print("📱 Initializing Telegram bot...")
#         telegram_service = get_telegram_service()
#         await telegram_service.initialize()
#         print("✅ Telegram bot initialized successfully")
#     except Exception as e:
#         print(f"⚠️ Telegram bot failed to initialize: {e}")
#         import traceback
#         traceback.print_exc()


@app.get("/api")
async def root() -> dict[str, str]:
    """
    API info endpoint.

    Returns:
        dict: Welcome message and API information
    """
    return {
        "message": "ADHD Coach API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/api/health")
async def health_check() -> dict[str, str | datetime]:
    """
    Health check endpoint.

    Returns:
        dict: Health status and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "service": "adhd-coach-backend"
    }

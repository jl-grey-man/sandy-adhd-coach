#!/usr/bin/env python3
"""
Telegram Bot Runner - keeps the bot alive and polling for messages.
Run this separately from the FastAPI server.
"""
import asyncio
import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.telegram_service import get_telegram_service
from app.services.reminder_scheduler import init_scheduler, start_scheduler, stop_scheduler
from app.database import SessionLocal

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def main():
    """Run the Telegram bot."""
    logger.info("🤖 Starting ADHD Coach Telegram Bot...")
    
    service = None
    scheduler = None
    
    try:
        # Initialize service
        service = get_telegram_service()
        await service.initialize()
        logger.info("✅ Bot initialized successfully!")
        
        # Initialize and start reminder scheduler
        scheduler = init_scheduler(service.bot, SessionLocal)
        await start_scheduler()
        logger.info("⏰ Reminder scheduler started!")
        
        # Start polling
        logger.info("📱 Polling for messages... (Press Ctrl+C to stop)")
        await service.application.updater.start_polling()
        
        # Keep running
        await asyncio.Event().wait()
        
    except KeyboardInterrupt:
        logger.info("⏹️ Stopping bot...")
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Stop scheduler
        if scheduler:
            await stop_scheduler()
            logger.info("⏰ Scheduler stopped")
        
        # Stop bot
        if service and service.application and service.application.updater:
            await service.application.updater.stop()
        logger.info("👋 Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())

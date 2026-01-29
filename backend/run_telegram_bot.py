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

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def main():
    """Run the Telegram bot."""
    logger.info("🤖 Starting ADHD Coach Telegram Bot...")
    
    try:
        # Initialize service
        service = get_telegram_service()
        await service.initialize()
        logger.info("✅ Bot initialized successfully!")
        
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
        if service.application and service.application.updater:
            await service.application.updater.stop()
        logger.info("👋 Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())

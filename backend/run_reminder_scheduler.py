"""Background scheduler for sending reminders."""
import asyncio
import logging
import os
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.reminder import Reminder
from app.models.user import User
from app.services.telegram_service import TelegramService
from app.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def check_and_send_reminders():
    """Check for due reminders and send them."""
    db = next(get_db())
    settings = get_settings()
    telegram_service = TelegramService(token=settings.telegram_bot_token)
    
    try:
        # Get all unsent reminders that are due
        now = datetime.utcnow()
        due_reminders = db.query(Reminder).filter(
            Reminder.sent == False,
            Reminder.remind_at <= now
        ).all()
        
        if due_reminders:
            logger.info(f"Found {len(due_reminders)} due reminders")
        
        for reminder in due_reminders:
            try:
                # Get user
                user = db.query(User).filter(User.id == reminder.user_id).first()
                
                if not user or not user.telegram_chat_id:
                    logger.warning(f"User {reminder.user_id} has no Telegram chat ID")
                    continue
                
                # Send reminder with Sandy's personality
                # Parse the reminder message to make it conversational
                task = reminder.message.lower()
                
                # Generate natural variations based on the task
                if "drink" in task and "water" in task:
                    human_reminders = [
                        "Hey! Time to drink that water, boss.",
                        "Don't forget to drink water.",
                        "Water break time!",
                        "Quick reminder - hydrate!",
                    ]
                elif "stretch" in task or "break" in task:
                    human_reminders = [
                        "Time to stretch, boss.",
                        "Get up and move around a bit.",
                        "Break time - go stretch.",
                        "You wanted me to remind you to take a break.",
                    ]
                else:
                    # Generic reminders
                    human_reminders = [
                        f"Hey boss - {reminder.message.lower()}",
                        f"Don't forget: {reminder.message.lower()}",
                        f"Quick reminder - {reminder.message.lower()}",
                        f"Time to {reminder.message.lower()}",
                    ]
                
                # Pick a random one for variety
                import random
                message = random.choice(human_reminders)
                
                await telegram_service.send_message(
                    chat_id=user.telegram_chat_id,
                    message=message,
                    parse_mode=None  # No markdown, just natural text
                )
                
                # Mark as sent
                reminder.sent = True
                db.commit()
                
                logger.info(f"Sent reminder {reminder.id} to user {user.id}")
                
            except Exception as e:
                logger.error(f"Failed to send reminder {reminder.id}: {e}")
                db.rollback()
    
    finally:
        db.close()


async def run_scheduler():
    """Run the reminder scheduler in a loop."""
    logger.info("🔔 Reminder scheduler started")
    
    while True:
        try:
            await check_and_send_reminders()
        except Exception as e:
            logger.error(f"Error in reminder scheduler: {e}")
        
        # Check every 30 seconds
        await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(run_scheduler())

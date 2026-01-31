"""
Background Scheduler for Reminders and Daily Updates
Runs periodic checks for due reminders and 9 AM updates
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional
from telegram import Bot
from .time_intelligence import TimeIntelligence

logger = logging.getLogger(__name__)


class ReminderScheduler:
    """Background scheduler for reminders and daily check-ins"""
    
    def __init__(self, bot: Bot, db_session_factory, check_interval: int = 60):
        """
        Initialize scheduler
        
        Args:
            bot: Telegram bot instance
            db_session_factory: Factory function that returns a DB session
            check_interval: How often to check for due reminders (seconds)
        """
        self.bot = bot
        self.db_session_factory = db_session_factory
        self.check_interval = check_interval
        self.running = False
        self._task: Optional[asyncio.Task] = None
        self._last_9am_check = None
    
    async def start(self):
        """Start the background scheduler"""
        if self.running:
            logger.warning("Scheduler already running")
            return
        
        self.running = True
        self._task = asyncio.create_task(self._run_loop())
        logger.info(f"Reminder scheduler started (checking every {self.check_interval}s)")
    
    async def stop(self):
        """Stop the background scheduler"""
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Reminder scheduler stopped")
    
    async def _run_loop(self):
        """Main scheduler loop"""
        while self.running:
            try:
                await self._check_reminders()
                await self._check_daily_update()
                await asyncio.sleep(self.check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}", exc_info=True)
                await asyncio.sleep(self.check_interval)
    
    async def _check_reminders(self):
        """Check for due reminders and send them"""
        db = self.db_session_factory()
        try:
            from ..models.reminder import Reminder
            
            now = TimeIntelligence.now()
            
            # Find reminders that are due (within the next check_interval seconds)
            due_window = now + timedelta(seconds=self.check_interval)
            
            due_reminders = db.query(Reminder).filter(
                Reminder.is_sent == False,
                Reminder.reminder_time <= due_window,
                Reminder.reminder_time > (now - timedelta(minutes=5))  # Grace period
            ).all()
            
            for reminder in due_reminders:
                try:
                    await self._send_reminder(reminder)
                    reminder.is_sent = True
                    reminder.sent_at = now
                    db.commit()
                    
                except Exception as e:
                    logger.error(f"Error sending reminder {reminder.id}: {e}", exc_info=True)
                    db.rollback()
            
            if due_reminders:
                logger.info(f"Processed {len(due_reminders)} due reminders")
                
        finally:
            db.close()
    
    async def _send_reminder(self, reminder):
        """Send a reminder to the user"""
        message = f"⏰ **Reminder!**\n\n{reminder.task}"
        
        if reminder.context:
            message += f"\n\n_Context: {reminder.context}_"
        
        await self.bot.send_message(
            chat_id=reminder.user_id,
            text=message,
            parse_mode='Markdown'
        )
        
        logger.info(f"Sent reminder {reminder.id} to user {reminder.user_id}")
    
    async def _check_daily_update(self):
        """Check if it's time for the 9 AM daily update"""
        now = TimeIntelligence.now()
        
        # Only check once per day around 9 AM
        if self._last_9am_check and self._last_9am_check.date() == now.date():
            return  # Already checked today
        
        # Check if it's 9 AM (within 5 minute window since we check every 60s)
        if now.hour == 9 and now.minute < 5:
            self._last_9am_check = now
            await self._send_daily_updates()
    
    async def _send_daily_updates(self):
        """Send 9 AM check-in to all active users"""
        db = self.db_session_factory()
        try:
            # For now, send to all users who have interacted with the bot
            # We'll get all unique user_ids from conversations
            from ..models.conversation import Conversation
            
            # Get unique user IDs
            user_ids = db.query(Conversation.user_id).distinct().all()
            user_ids = [uid[0] for uid in user_ids]
            
            for user_id in user_ids:
                try:
                    message = (
                        "🌅 **Good morning!**\n\n"
                        "New day, fresh start! What's one thing you want to accomplish today?\n\n"
                        "I'm here if you need help breaking it down or staying on track."
                    )
                    
                    await self.bot.send_message(
                        chat_id=user_id,
                        text=message,
                        parse_mode='Markdown'
                    )
                    
                    logger.info(f"Sent daily update to user {user_id}")
                    
                except Exception as e:
                    logger.error(f"Error sending daily update to user {user_id}: {e}")
            
            logger.info(f"Sent daily updates to {len(user_ids)} users")
            
        finally:
            db.close()


# Global scheduler instance (initialized in main app)
_scheduler: Optional[ReminderScheduler] = None


def init_scheduler(bot: Bot, db_session_factory):
    """Initialize the global scheduler"""
    global _scheduler
    _scheduler = ReminderScheduler(bot, db_session_factory)
    return _scheduler


def get_scheduler() -> Optional[ReminderScheduler]:
    """Get the global scheduler instance"""
    return _scheduler


async def start_scheduler():
    """Start the global scheduler"""
    if _scheduler:
        await _scheduler.start()
    else:
        logger.error("Scheduler not initialized. Call init_scheduler first.")


async def stop_scheduler():
    """Stop the global scheduler"""
    if _scheduler:
        await _scheduler.stop()

"""
AI Actions Service - Updated with Time Intelligence
Handles reminder creation with natural language time parsing
"""
from datetime import datetime
from typing import Optional, Dict, Any
import logging
from .time_intelligence import TimeIntelligence

logger = logging.getLogger(__name__)


class AIActionsService:
    """Handles AI-initiated actions like reminder creation"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    async def create_reminder(
        self,
        user_id: int,
        task: str,
        time_expression: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a reminder with natural language time parsing.
        
        Args:
            user_id: User's Telegram ID
            task: What to remind about
            time_expression: Natural language time (e.g., "tomorrow at 12", "in 30 minutes")
            context: Optional context about why this reminder was created
        
        Returns:
            Dict with success status, reminder details, and any errors
        """
        try:
            # Parse the time expression
            reminder_time = TimeIntelligence.parse_reminder_time(time_expression)
            
            if reminder_time is None:
                return {
                    "success": False,
                    "error": f"Couldn't understand the time '{time_expression}'. Try formats like 'tomorrow at 12:00', 'in 30 minutes', or 'Thursday at 14:22'"
                }
            
            # Ensure reminder is in the future
            now = TimeIntelligence.now()
            if reminder_time <= now:
                return {
                    "success": False,
                    "error": f"That time has already passed. Current time is {now.strftime('%H:%M')}"
                }
            
            # Store in database
            from ..models.reminder import Reminder
            
            reminder = Reminder(
                user_id=user_id,
                task=task,
                reminder_time=reminder_time,
                context=context,
                created_at=now,
                is_sent=False
            )
            
            self.db.add(reminder)
            self.db.commit()
            self.db.refresh(reminder)
            
            # Format friendly response
            friendly_time = TimeIntelligence.format_time_friendly(reminder_time)
            
            logger.info(f"Created reminder for user {user_id}: '{task}' at {reminder_time}")
            
            return {
                "success": True,
                "reminder_id": reminder.id,
                "task": task,
                "reminder_time": reminder_time.isoformat(),
                "friendly_time": friendly_time,
                "message": f"Got it! I'll remind you about '{task}' {friendly_time}."
            }
            
        except Exception as e:
            logger.error(f"Error creating reminder: {e}", exc_info=True)
            return {
                "success": False,
                "error": f"Failed to create reminder: {str(e)}"
            }
    
    async def list_reminders(self, user_id: int, include_past: bool = False) -> Dict[str, Any]:
        """List all reminders for a user"""
        try:
            from ..models.reminder import Reminder
            
            query = self.db.query(Reminder).filter(Reminder.user_id == user_id)
            
            if not include_past:
                now = TimeIntelligence.now()
                query = query.filter(Reminder.reminder_time > now)
            
            reminders = query.order_by(Reminder.reminder_time).all()
            
            reminder_list = []
            for r in reminders:
                reminder_list.append({
                    "id": r.id,
                    "task": r.task,
                    "time": r.reminder_time.isoformat(),
                    "friendly_time": TimeIntelligence.format_time_friendly(r.reminder_time),
                    "is_sent": r.is_sent
                })
            
            return {
                "success": True,
                "count": len(reminder_list),
                "reminders": reminder_list
            }
            
        except Exception as e:
            logger.error(f"Error listing reminders: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
    
    async def delete_reminder(self, user_id: int, reminder_id: int) -> Dict[str, Any]:
        """Delete a reminder"""
        try:
            from ..models.reminder import Reminder
            
            reminder = self.db.query(Reminder).filter(
                Reminder.id == reminder_id,
                Reminder.user_id == user_id
            ).first()
            
            if not reminder:
                return {
                    "success": False,
                    "error": "Reminder not found"
                }
            
            task = reminder.task
            self.db.delete(reminder)
            self.db.commit()
            
            return {
                "success": True,
                "message": f"Deleted reminder: '{task}'"
            }
            
        except Exception as e:
            logger.error(f"Error deleting reminder: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }


# Function-based interface for backward compatibility
async def create_reminder_action(
    db_session,
    user_id: int,
    task: str,
    time_expression: str,
    context: Optional[str] = None
) -> Dict[str, Any]:
    """Create a reminder with natural language time parsing"""
    service = AIActionsService(db_session)
    return await service.create_reminder(user_id, task, time_expression, context)


def extract_actions_from_response(response: str) -> list:
    """
    Extract AI action tags from Sandy's response.
    
    Looks for: <ai_action type="create_reminder">...</ai_action>
    
    Returns list of action dicts with parsed data
    """
    import re
    
    actions = []
    
    # Pattern for reminder actions
    pattern = r'<ai_action type="create_reminder">\s*<task>(.*?)</task>\s*<time>(.*?)</time>(?:\s*<context>(.*?)</context>)?\s*</ai_action>'
    matches = re.findall(pattern, response, re.DOTALL)
    
    for task, time_expr, context in matches:
        actions.append({
            "type": "create_reminder",
            "task": task.strip(),
            "time": time_expr.strip(),
            "context": context.strip() if context else None
        })
    
    return actions


def execute_action(action: dict, user_id: int, db_session) -> Dict[str, Any]:
    """
    Execute an AI action and return result.
    
    Currently supports:
    - create_reminder: Create a new reminder
    
    Returns dict with success status and details
    """
    import asyncio
    
    action_type = action.get("type")
    
    if action_type == "create_reminder":
        # Run async function synchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                create_reminder_action(
                    db_session=db_session,
                    user_id=user_id,
                    task=action["task"],
                    time_expression=action["time"],
                    context=action.get("context")
                )
            )
            
            return {
                "success": result["success"],
                "action_type": "create_reminder",
                "details": result
            }
        finally:
            loop.close()
    
    return {
        "success": False,
        "action_type": action_type,
        "details": {"error": f"Unknown action type: {action_type}"}
    }

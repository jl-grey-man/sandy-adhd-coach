"""Time intelligence service for parsing natural language time expressions."""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import re
from typing import Optional
from sqlalchemy.orm import Session


class TimeIntelligence:
    """Parse natural language time expressions into timezone-aware datetime objects."""
    
    TIMEZONE = ZoneInfo("Europe/Stockholm")
    
    def __init__(self, user_id: int, db: Session):
        """Initialize with user and database context."""
        self.user_id = user_id
        self.db = db
    
    @classmethod
    def parse_reminder_time(cls, time_expression: str) -> Optional[datetime]:
        """
        Parse natural language time expression into timezone-aware datetime.
        
        Supported formats:
        - "in X minutes/hours/days"
        - "tomorrow at HH:MM"
        - "Monday/Tuesday/etc at HH:MM"
        - "at HH:MM" (today)
        
        Args:
            time_expression: Natural language time expression
            
        Returns:
            Timezone-aware datetime object in Europe/Stockholm timezone, or None if parsing fails
        """
        time_expression = time_expression.lower().strip()
        now = datetime.now(cls.TIMEZONE)
        
        # Pattern: "in X minutes/hours/days"
        relative_match = re.match(r'in (\d+)\s*(minute|minutes|hour|hours|day|days)', time_expression)
        if relative_match:
            amount = int(relative_match.group(1))
            unit = relative_match.group(2)
            
            if 'minute' in unit:
                return now + timedelta(minutes=amount)
            elif 'hour' in unit:
                return now + timedelta(hours=amount)
            elif 'day' in unit:
                return now + timedelta(days=amount)
        
        # Pattern: "tomorrow at HH:MM"
        tomorrow_match = re.match(r'tomorrow\s+at\s+(\d{1,2}):(\d{2})', time_expression)
        if tomorrow_match:
            hour = int(tomorrow_match.group(1))
            minute = int(tomorrow_match.group(2))
            tomorrow = now + timedelta(days=1)
            return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Pattern: "at HH:MM" (today)
        at_time_match = re.match(r'at\s+(\d{1,2}):(\d{2})', time_expression)
        if at_time_match:
            hour = int(at_time_match.group(1))
            minute = int(at_time_match.group(2))
            target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If time has passed today, schedule for tomorrow
            if target_time <= now:
                target_time += timedelta(days=1)
            
            return target_time
        
        # Pattern: "Monday/Tuesday/etc at HH:MM"
        weekday_match = re.match(
            r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s+at\s+(\d{1,2}):(\d{2})',
            time_expression
        )
        if weekday_match:
            weekday_name = weekday_match.group(1)
            hour = int(weekday_match.group(2))
            minute = int(weekday_match.group(3))
            
            weekday_map = {
                'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                'friday': 4, 'saturday': 5, 'sunday': 6
            }
            target_weekday = weekday_map[weekday_name]
            current_weekday = now.weekday()
            
            # Calculate days until target weekday
            days_ahead = target_weekday - current_weekday
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            
            target_date = now + timedelta(days=days_ahead)
            return target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        return None
    
    @classmethod
    def now(cls) -> datetime:
        """Get current time in Europe/Stockholm timezone."""
        return datetime.now(cls.TIMEZONE)
    
    def get_capacity_summary(self) -> dict:
        """Get capacity analysis - stub for now."""
        return {
            "status": "unknown",
            "message": "Capacity analysis not yet implemented"
        }

"""
Time Intelligence Service for Sandy
Handles timezone-aware time parsing and reminder scheduling
"""
from datetime import datetime, timedelta
from typing import Optional, Tuple
import re
from zoneinfo import ZoneInfo

# User timezone - Sweden
USER_TIMEZONE = ZoneInfo("Europe/Stockholm")


def get_current_time() -> datetime:
    """Get current time in user's timezone (Sweden)"""
    return datetime.now(USER_TIMEZONE)


def parse_reminder_time(text: str, reference_time: Optional[datetime] = None) -> Optional[datetime]:
    """
    Parse natural language time expressions into datetime objects.
    
    Handles:
    - "in X minutes/hours/days"
    - "tomorrow at HH:MM"
    - "Monday/Tuesday/etc at HH:MM"
    - "at HH:MM" (today)
    - "YYYY-MM-DD HH:MM"
    
    Args:
        text: Natural language time expression
        reference_time: Reference datetime (defaults to current time in Sweden)
    
    Returns:
        datetime object in Sweden timezone, or None if parsing fails
    """
    if reference_time is None:
        reference_time = get_current_time()
    
    text = text.lower().strip()
    
    # Pattern: "in X minutes/hours/days/weeks"
    relative_match = re.search(r'in\s+(\d+)\s+(minute|hour|day|week)s?', text)
    if relative_match:
        amount = int(relative_match.group(1))
        unit = relative_match.group(2)
        
        if unit == 'minute':
            return reference_time + timedelta(minutes=amount)
        elif unit == 'hour':
            return reference_time + timedelta(hours=amount)
        elif unit == 'day':
            return reference_time + timedelta(days=amount)
        elif unit == 'week':
            return reference_time + timedelta(weeks=amount)
    
    # Pattern: "tomorrow at HH:MM" or "tomorrow HH:MM"
    tomorrow_match = re.search(r'tomorrow\s+(?:at\s+)?(\d{1,2})[:.h](\d{2})', text)
    if tomorrow_match:
        hour = int(tomorrow_match.group(1))
        minute = int(tomorrow_match.group(2))
        target = reference_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
        target += timedelta(days=1)
        return target
    
    # Pattern: "Monday/Tuesday/etc at HH:MM"
    days_of_week = {
        'monday': 0, 'mon': 0, 'måndag': 0,
        'tuesday': 1, 'tue': 1, 'tisdag': 1,
        'wednesday': 2, 'wed': 2, 'onsdag': 2,
        'thursday': 3, 'thu': 3, 'torsdag': 3,
        'friday': 4, 'fri': 4, 'fredag': 4,
        'saturday': 5, 'sat': 5, 'lördag': 5,
        'sunday': 6, 'sun': 6, 'söndag': 6,
    }
    
    for day_name, day_num in days_of_week.items():
        day_pattern = rf'{day_name}\s+(?:at\s+)?(\d{{1,2}})[:.h](\d{{2}})'
        day_match = re.search(day_pattern, text)
        if day_match:
            hour = int(day_match.group(1))
            minute = int(day_match.group(2))
            
            # Calculate days until target day
            current_day = reference_time.weekday()
            days_ahead = day_num - current_day
            if days_ahead <= 0:  # Target day is today or has passed this week
                days_ahead += 7  # Move to next week
            
            target = reference_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
            target += timedelta(days=days_ahead)
            return target
    
    # Pattern: "at HH:MM" or just "HH:MM" (today)
    time_match = re.search(r'(?:at\s+)?(\d{1,2})[:.h](\d{2})', text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2))
        target = reference_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # If time has passed today, assume tomorrow
        if target <= reference_time:
            target += timedelta(days=1)
        return target
    
    # Pattern: ISO format "YYYY-MM-DD HH:MM"
    iso_match = re.search(r'(\d{4})-(\d{2})-(\d{2})\s+(\d{1,2})[:.h](\d{2})', text)
    if iso_match:
        year = int(iso_match.group(1))
        month = int(iso_match.group(2))
        day = int(iso_match.group(3))
        hour = int(iso_match.group(4))
        minute = int(iso_match.group(5))
        return datetime(year, month, day, hour, minute, tzinfo=USER_TIMEZONE)
    
    return None


def format_time_friendly(dt: datetime) -> str:
    """Format datetime in a friendly way for display"""
    now = get_current_time()
    
    # Calculate time difference
    diff = dt - now
    
    # If it's today
    if dt.date() == now.date():
        return f"today at {dt.strftime('%H:%M')}"
    
    # If it's tomorrow
    if dt.date() == (now + timedelta(days=1)).date():
        return f"tomorrow at {dt.strftime('%H:%M')}"
    
    # If within the next week
    if 0 < diff.days <= 7:
        day_name = dt.strftime('%A')
        return f"{day_name} at {dt.strftime('%H:%M')}"
    
    # Otherwise show date
    return dt.strftime('%Y-%m-%d at %H:%M')


def should_send_daily_update() -> bool:
    """Check if it's time for the 9 AM daily update"""
    now = get_current_time()
    return now.hour == 9 and now.minute < 5  # 5-minute window


def get_next_9am() -> datetime:
    """Get the next 9 AM time in Sweden timezone"""
    now = get_current_time()
    next_9am = now.replace(hour=9, minute=0, second=0, microsecond=0)
    
    if now.hour >= 9:
        next_9am += timedelta(days=1)
    
    return next_9am


# Example usage and tests
if __name__ == "__main__":
    now = get_current_time()
    print(f"Current time in Sweden: {now}")
    
    test_cases = [
        "in 5 minutes",
        "in 2 hours",
        "tomorrow at 12:00",
        "Thursday at 14:22",
        "at 15:30",
        "monday at 9:00"
    ]
    
    print("\nTest cases:")
    for test in test_cases:
        result = parse_reminder_time(test)
        if result:
            print(f"'{test}' -> {format_time_friendly(result)} ({result})")
        else:
            print(f"'{test}' -> Failed to parse")

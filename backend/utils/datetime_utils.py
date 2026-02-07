"""
Date and time utility functions for the application
"""

from datetime import datetime
from typing import Optional
import pytz


def utc_now() -> datetime:
    """Return current time in UTC"""
    return datetime.now(pytz.UTC)


def is_future_datetime(dt: Optional[datetime]) -> bool:
    """Check if a datetime is in the future"""
    if dt is None:
        return False
    utc_dt = dt.astimezone(pytz.UTC) if dt.tzinfo else pytz.UTC.localize(dt)
    return utc_dt > utc_now()


def validate_utc_datetime(dt: Optional[datetime]) -> bool:
    """Validate that datetime is in UTC"""
    if dt is None:
        return True
    return dt.tzinfo is not None and dt.tzinfo.zone == 'UTC'


def validate_recurrence_rule(rrule: Optional[str]) -> bool:
    """Validate that recurrence rule follows RFC 5545 format"""
    if not rrule:
        return True

    # Basic validation for RRULE format
    rrule = rrule.strip().upper()
    if not rrule.startswith('RRULE:'):
        return False

    # Check for required components in a basic way
    # This is a simplified validation - a full RFC 5545 validator would be more complex
    parts = rrule[6:].split(';')  # Remove 'RRULE:' prefix
    has_freq = any(part.startswith('FREQ=') for part in parts)

    return has_freq


def create_rrule_datetime(dt: datetime) -> str:
    """Convert a datetime to an RFC 3339 string in UTC"""
    if dt.tzinfo is None:
        dt = pytz.UTC.localize(dt)
    else:
        dt = dt.astimezone(pytz.UTC)
    return dt.isoformat()


def parse_rrule_datetime(dt_str: str) -> Optional[datetime]:
    """Parse an RFC 3339 datetime string to datetime object in UTC"""
    try:
        from datetime import datetime
        # Handle various datetime formats
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        if dt.tzinfo is None:
            dt = pytz.UTC.localize(dt)
        else:
            dt = dt.astimezone(pytz.UTC)
        return dt
    except ValueError:
        return None
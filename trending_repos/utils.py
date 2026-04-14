"""
utils.py
--------
Utility functions for the trending-repos CLI tool.
Currently handles: converting a duration string into a 'YYYY-MM-DD' date
that we pass to the GitHub Search API.
"""

from datetime import datetime, timedelta


# Maps user-friendly duration names to how many days back we look
DURATION_DAYS = {
    "day":   1,
    "week":  7,
    "month": 30,
    "year":  365,
}

VALID_DURATIONS = list(DURATION_DAYS.keys())


def get_start_date(duration: str) -> str:
    """
    Convert a duration string like 'week' into a date string like '2024-12-01'.

    Why do we need this?
    The GitHub Search API doesn't understand "last week". It only understands
    real dates. So we calculate: today minus N days = the start date.

    Args:
        duration: one of 'day', 'week', 'month', 'year'

    Returns:
        A date string in 'YYYY-MM-DD' format

    Example:
        get_start_date('week')  →  '2024-12-20'  (if today is 2024-12-27)
    """
    if duration not in DURATION_DAYS:
        raise ValueError(
            f"Invalid duration '{duration}'. "
            f"Choose from: {', '.join(VALID_DURATIONS)}"
        )

    days_back = DURATION_DAYS[duration]
    start_date = datetime.utcnow() - timedelta(days=days_back)

    # GitHub API wants the format YYYY-MM-DD
    return start_date.strftime("%Y-%m-%d")


def validate_limit(limit: int) -> int:
    """
    Make sure the limit is a sensible number.
    GitHub's Search API returns max 100 results per page,
    so we cap it there.

    Args:
        limit: the number of repos the user wants to see

    Returns:
        A clamped integer between 1 and 100
    """
    if limit < 1:
        raise ValueError("--limit must be at least 1.")
    if limit > 100:
        raise ValueError("--limit cannot exceed 100 (GitHub API maximum).")
    return limit

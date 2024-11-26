from datetime import date, timedelta
from typing import Union

from langchain_core.tools import tool


@tool
def travel_dates(start: Union[date, str], end: Union[date, str]) -> dict:
    """
    Calculates travel dates.

    Args:
        start (Union[date, str]): Travel start date
        end (Union[date, str]): Travel end date

    Returns:
        dict: A dictionary
    """
    if isinstance(start, str):
        start = date.fromisoformat(start)
    if isinstance(end, str):
        end = date.fromisoformat(end)

    diff: timedelta = end - start
    return {
        "days": diff.days,
        "start_month": start.strftime("%B"),
        "end_month": end.strftime("%B"),
    }

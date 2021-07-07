from typing import *
from utils.remote_time import get_remote_utc_datetime
import datetime as dt


def parse_time(s: str) -> dt.time:
    return dt.datetime.strptime(s, "%H:%M")


def replace_time(d: dt.datetime, t: dt.time) -> dt.datetime:
    return d.replace(hour=t.hour, minute=t.minute)


def parse_replace_time(now: dt.datetime, s: str) -> dt.datetime:
    return replace_time(now, parse_time(s))


def get_now(timezone, use_remote: Optional[bool], parse_time: Optional[str]) -> Optional[dt.datetime]:
    """
    >>> utc = dt.timezone.utc
    >>> measure = dt.datetime.now().astimezone(dt.timezone.utc)
    >>> system = get_now(utc, use_remote=None, parse_time=None)
    >>> 0 <= system.timestamp() - measure.timestamp() < 1
    True

    >>> remote = get_now(utc, use_remote=True, parse_time=False)
    >>> abs(remote.timestamp() - measure.timestamp()) < 80
    True

    >>> parsed = get_now(utc, use_remote=False, parse_time=measure.strftime("%H:%M"))
    >>> abs(measure.timestamp() - parsed.timestamp()) < 10
    True
    >>> 
    """

    system = dt.datetime.now().astimezone(timezone)

    if use_remote:
        remote = get_remote_utc_datetime()

        if remote is None:
            if parse_time:
                return parse_replace_time(system, parse_time)
            else:
                return None
        else:
            return remote.astimezone(timezone)

    if parse_time:
        return parse_replace_time(system, parse_time)

    return system

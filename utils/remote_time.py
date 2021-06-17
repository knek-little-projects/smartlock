from typing import *
import datetime as dt
import requests
import logging


def _currentmillis_com():
    """
    >>> d1 = dt.datetime.now(dt.timezone.utc)
    >>> d2 = _currentmillis_com()
    >>> abs(d1.timestamp() - d2.timestamp()) < 60
    True
    >>>
    """
    response = requests.get("https://currentmillis.com/time/minutes-since-unix-epoch.php")
    minutes = int(response.text)
    ts = minutes * 60
    date = dt.datetime.utcfromtimestamp(ts).replace(tzinfo=dt.timezone.utc)
    return date


# def _tercdate():
#     s = requests.get("https://terc.app").headers.get("Date")
#     d = dateutil.parser.parse(s)
#     d = d.astimezone(dateutil.tz.gettz('MSC'))
#     return d


def get_remote_utc_datetime() -> Optional[dt.datetime]:
    """
    >>> d1 = dt.datetime.now(dt.timezone.utc)
    >>> d2 = get_remote_utc_datetime()
    >>> abs(d1.timestamp() - d2.timestamp()) < 60
    True
    >>>
    """
    try:
        return _currentmillis_com()
    except Exception as e:
        logging.error(str(e))

    return None

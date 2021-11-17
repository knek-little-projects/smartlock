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


def _pkradius_ru():
    """
    >>> d1 = dt.datetime.now(dt.timezone.utc)
    >>> d2 = _pkradius_ru()
    >>> abs(d1.timestamp() - d2.timestamp()) < 60
    True
    >>>
    """
    ts = requests.get("http://pkradius.ru:12345/ts").json()
    return dt.datetime.utcfromtimestamp(ts).replace(tzinfo=dt.timezone.utc)


def get_remote_utc_datetime() -> Optional[dt.datetime]:
    """
    >>> d1 = dt.datetime.now(dt.timezone.utc)
    >>> d2 = get_remote_utc_datetime()
    >>> abs(d1.timestamp() - d2.timestamp()) < 60
    True
    >>>
    """
    for remote_utc_datetime in _currentmillis_com, _pkradius_ru:
        try:
            return remote_utc_datetime()
        except Exception as e:
            logging.error(str(e))

    return None

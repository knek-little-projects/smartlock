from typing import *
from datetime import time as Time
from datetime import datetime as Datetime
from abc import ABC, abstractmethod


def is_seq(a, b, c):
    """
    >>> is_seq(Time(10), Time(12), Time(14))
    True
    >>> is_seq(Time(23), Time(1), Time(4))
    True
    >>> is_seq(Time(10), Time(1), Time(00))
    False
    """
    if a < c:
        return a <= b < c
    else:
        return a <= b or b < c


class Period(ABC):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @abstractmethod
    def __contains__(self, now: Datetime):
        pass


class TimePeriod(Period):
    @classmethod
    def parse(self, text) -> "TimePeriod":
        """
        >>> p = TimePeriod.parse("10:00 20:00")
        >>> p.start == Time(10)
        True
        >>> p.end == Time(20)
        True
        >>>
        """
        a, b = map(lambda s: Datetime.strptime(s, "%H:%M").time(), text.split())
        return TimePeriod(a, b)

    def __contains__(self, now: Union[Datetime, Time]):
        """
        >>> period = TimePeriod(Time(10, 0), Time(9, 0))
        >>> Time(11, 0) in period
        True
        >>> Time(8, 0) in period
        True
        >>> Time(9, 30) in period
        False
        >>> Datetime(10, 10, 10, 8, 0) in period
        True
        >>> Datetime(10, 10, 10, 9, 30) in period
        False
        >>> 
        """
        if isinstance(now, Datetime):
            now = now.time()

        return is_seq(self.start, now, self.end)


class DatetimePeriod(Period):
    def __init__(self, start: Datetime, end: Datetime):
        assert start < end
        super().__init__(start, end)

    def __contains__(self, datetime: Datetime):
        """
        >>> period = DatetimePeriod(Datetime(9, 9, 9, 9, 9), Datetime(12, 12, 12, 12, 12))
        >>> now = Datetime(11, 11, 11, 11, 11)
        >>> now in period
        True
        >>> 
        """
        return self.start < datetime < self.end


def parse_time_periods(periods):
    return [TimePeriod.parse(p) for p in periods] if periods is not None else None
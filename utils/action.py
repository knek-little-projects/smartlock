from typing import *
from enum import Enum, auto
from utils.period import Period
from utils.period import DatetimePeriod, TimePeriod, Time, Datetime  # for doc tests


class Action(Enum):
    BLOCK_USER = auto()
    BLOCK_ADMIN = auto()
    BLOCK_ACTIVITIES = auto()
    UNBLOCK_USER = auto()
    UNBLOCK_ADMIN = auto()
    UNBLOCK_ACTIVITIES = auto()
    LOCK_USER_SCREEN = auto()
    UNLOCK_USER_SCREEN = auto()


ALLOW_ALL = [
    Action.UNBLOCK_USER,
    Action.UNBLOCK_ADMIN,
    Action.UNBLOCK_ACTIVITIES,
    Action.UNLOCK_USER_SCREEN,
]

BLOCK_ALL = [
    Action.BLOCK_USER,
    Action.BLOCK_ADMIN,
    Action.BLOCK_ACTIVITIES,
    Action.LOCK_USER_SCREEN,
]


def _is_activity_allowed(
    now: Datetime,
    is_activity_positive: Optional[int],
    allowed_periods: Optional[List[Period]]
):
    """
    >>> allowed_time = Datetime(10, 10, 10)
    >>> allowed_periods = [DatetimePeriod(Datetime(1,1,1), Datetime(11,11,11))]
    >>> allowed_time in allowed_periods[0]
    True
    >>> _is_activity_allowed(allowed_time, None, None)
    True
    >>> _is_activity_allowed(allowed_time, True, None)
    True
    >>> _is_activity_allowed(allowed_time, False, None)
    False
    >>> _is_activity_allowed(allowed_time, True, allowed_periods)
    True
    >>> _is_activity_allowed(allowed_time, False, allowed_periods)
    False
    >>> _is_activity_allowed(allowed_time, None, allowed_periods)
    True
    >>> disallowed_time = Datetime(12, 12, 12)
    >>> disallowed_time in allowed_periods[0]
    False
    >>> _is_activity_allowed(disallowed_time, True, allowed_periods)
    False
    >>> _is_activity_allowed(disallowed_time, False, allowed_periods)
    False
    >>> 
    """
    if allowed_periods is not None:
        if not any(now in period for period in allowed_periods):
            return False

    if is_activity_positive is not None:
        return is_activity_positive

    return True


def compute_actions(
    now: Datetime,
    is_activity_positive: Optional[bool] = None,
    allowed_activity_periods: Optional[List[Period]] = None,
    danger_periods: Optional[List[Period]] = None,
    critical_periods: Optional[List[Period]] = None,
    allow_all_periods: Optional[List[Period]] = None,
    dinner_periods: Optional[List[Period]] = None,
) -> List[Action]:
    """
    >>> def P(actions):
    ...   print(" ".join(action.name for action in actions))
    ...

    >>> allow_all_periods = [DatetimePeriod(Datetime(1, 1, 1), Datetime(11, 11, 11))]
    >>> P(compute_actions(Datetime(5, 5, 5), allow_all_periods=allow_all_periods))
    UNBLOCK_USER UNBLOCK_ADMIN UNBLOCK_ACTIVITIES UNLOCK_USER_SCREEN

    >>> P(compute_actions(Datetime(5, 5, 5)))
    UNBLOCK_ACTIVITIES UNBLOCK_ADMIN UNBLOCK_USER UNLOCK_USER_SCREEN

    >>> danger_periods = [TimePeriod(Time(14), Time(1))]
    >>> P(compute_actions(Datetime(5, 5, 5, 10), danger_periods=danger_periods))
    UNBLOCK_ACTIVITIES UNBLOCK_ADMIN UNBLOCK_USER UNLOCK_USER_SCREEN
    
    >>> P(compute_actions(Datetime(5, 5, 5, 0, 30), danger_periods=danger_periods))
    UNBLOCK_ACTIVITIES BLOCK_ADMIN UNBLOCK_USER UNLOCK_USER_SCREEN

    >>> critical_periods = [TimePeriod(Time(1), Time(4))]
    >>> P(compute_actions(Datetime(5, 5, 5, 10, 0), danger_periods=danger_periods, critical_periods=critical_periods))
    UNBLOCK_ACTIVITIES UNBLOCK_ADMIN UNBLOCK_USER UNLOCK_USER_SCREEN
    
    >>> P(compute_actions(Datetime(5, 5, 5, 0, 0), danger_periods=danger_periods, critical_periods=critical_periods))
    UNBLOCK_ACTIVITIES BLOCK_ADMIN UNBLOCK_USER UNLOCK_USER_SCREEN
    
    >>> compute_actions(Datetime(5, 5, 5, 1, 30), danger_periods=danger_periods, critical_periods=critical_periods) == BLOCK_ALL
    True
    
    >>> 
    """

    if now is None:
        return BLOCK_ALL

    if allow_all_periods is not None:
        if any(now in period for period in allow_all_periods):
            return ALLOW_ALL

    actions = []

    if _is_activity_allowed(now, is_activity_positive, allowed_activity_periods):
        actions.append(Action.UNBLOCK_ACTIVITIES)
    else:
        actions.append(Action.BLOCK_ACTIVITIES)

    if any(now in period for period in critical_periods or []):
        return BLOCK_ALL

    elif any(now in period for period in danger_periods or []):
        actions.append(Action.BLOCK_ADMIN)
        actions.append(Action.UNBLOCK_USER)

    else:
        actions.append(Action.UNBLOCK_ADMIN)
        actions.append(Action.UNBLOCK_USER)

    if any(now in period for period in dinner_periods or []):
        actions.append(Action.LOCK_USER_SCREEN)
    else:
        actions.append(Action.UNLOCK_USER_SCREEN)

    return actions

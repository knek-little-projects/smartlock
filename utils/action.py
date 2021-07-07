from typing import *
from enum import Enum, auto
from utils.period import Period, DatetimePeriod, TimePeriod, Time, Datetime  # for doc tests
from utils.rules import Rule, ApplyFlag, ApplyAction, ApplyBreak
import requests


def compute_actions(now: Datetime, flags: Dict[str, Any], rules: List[Rule]) -> Iterator[str]:
    for rule in rules:
        for apply in rule.applies(rule.get_value(now=now, flags=flags)):
            if isinstance(apply, ApplyFlag):
                flags[apply.flag] = apply.value

            elif isinstance(apply, ApplyAction):
                yield apply.action

            elif isinstance(apply, ApplyBreak):
                return

            else:
                raise Exception("Apply %s wasn't handled" % type(apply))

from typing import *
from dataclasses import dataclass
from utils.action import Action
from utils.period import Period, TimePeriod, parse_time_periods
import datetime as dt
import yaml


@dataclass
class Config:
    shell: str
    shell_encoding: str
    env: Dict[str, str]
    commands: Dict[Action, str]
    timezone: dt.timezone
    is_activity_allowed_url: str
    allowed_activity_periods: Optional[List[Period]] = None
    danger_periods: Optional[List[Period]] = None
    dinner_periods: Optional[List[Period]] = None
    critical_periods: Optional[List[Period]] = None
    allow_all_periods: Optional[List[Period]] = None

    @classmethod
    def parse_yaml(cls, text):
        data = yaml.safe_load(text)
        return Config(
            shell=data.get("shell", "/bin/sh"),
            shell_encoding=data.get("shell_encoding", "UTF-8"),
            env=data["env"],
            commands=data["commands"],
            is_activity_allowed_url=data["is_activity_allowed_url"],
            timezone=dt.timezone(dt.timedelta(hours=int(data["timezone"]))),
            allowed_activity_periods=parse_time_periods(data["allowed_activity_periods"]),
            danger_periods=parse_time_periods(data["danger_periods"]),
            dinner_periods=parse_time_periods(data["dinner_periods"]),
            critical_periods=parse_time_periods(data["critical_periods"]),
            allow_all_periods=parse_time_periods(data["allow_all_periods"]),
        )

    @classmethod
    def parse_file(cls, path):
        with open(path) as input:
            return cls.parse_yaml(input.read())

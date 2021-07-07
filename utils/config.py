from typing import *
from dataclasses import dataclass
from utils.rules import parse_rules
import datetime as dt


@dataclass
class Config:
    shell: str
    shell_encoding: str
    global_env: Dict[str, str]
    env: Dict[str, str]
    actions: Dict[str, str]
    timezone: dt.timezone
    flags: Dict[str, Any]
    rules: List[Dict[str, Any]]

    @classmethod
    def parse(cls, data: Dict[str, Any]):
        assert data["actions"]["FAILSAFE"]

        return Config(
            shell=data.get("shell", "/bin/sh"),
            shell_encoding=data.get("shell_encoding", "UTF-8"),
            global_env=data["global_env"],
            env=data["env"],
            actions=data["actions"],
            flags=data["flags"],
            rules=parse_rules(data["rules"]),
            timezone=dt.timezone(dt.timedelta(hours=int(data["timezone"]))),
        )
        
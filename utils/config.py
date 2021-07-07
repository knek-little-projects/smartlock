from typing import *
from dataclasses import dataclass
from utils.rules import parse_rules, RuleFlag, ApplyAction, ApplyFlag
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
    failsafe: str

    @classmethod
    def parse(cls, data: Dict[str, Any]):
        available_flags = set(data["flags"])
        available_actions = set(data["actions"])
        rules = list(parse_rules(data["rules"]))
        
        for rule in rules:
            if isinstance(rule, RuleFlag):
                assert rule.flag in available_flags, "Unknown flag: %s" % rule.flag

            for match in rule.matches:
                for apply in match.applies:
                    if isinstance(apply, ApplyFlag):
                        assert apply.flag in available_flags, "Unknown flag: %s" % apply.flag

                    elif isinstance(apply, ApplyAction):
                        assert apply.action in available_actions, "Unknown action: %s" % apply.action

        return Config(
            shell=data.get("shell", "/bin/sh"),
            shell_encoding=data.get("shell_encoding", "UTF-8"),
            global_env=data["global_env"],
            env=data["env"],
            actions=data["actions"],
            failsafe=data["actions"]["FAILSAFE"],
            flags=data["flags"],
            rules=rules,
            timezone=dt.timezone(dt.timedelta(hours=int(data["timezone"]))),
        )

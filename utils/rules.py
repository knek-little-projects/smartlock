from typing import *
from abc import ABC, abstractmethod, abstractclassmethod
from utils.period import parse_time_periods, TimePeriod, Datetime
import requests
import logging


class Apply(ABC):
    pass


class ApplyFlag(Apply):
    def __init__(self, flag, value):
        self.flag = flag
        self.value = value


class ApplyAction(Apply):
    def __init__(self, action):
        self.action = action


def parse_apply(data: Dict[str, Any]) -> Apply:
    data = dict(data)
    return globals()['Apply' + data.pop("type").capitalize()](**data)


def parse_applies(items: List[Dict[str, Any]]) -> Iterator[Apply]:
    return map(parse_apply, items)


class Match(ABC):
    def __init__(self, applies: List[Apply]):
        self.applies = applies

    @classmethod
    def parse(cls, data) -> "Match":
        data["applies"] = parse_applies(data["applies"])
        return cls(**data)

    @abstractmethod
    def test(self, value) -> bool:
        pass


class MatchValue(Match):
    def __init__(self, value, applies: List[Apply]):
        super().__init__(applies)
        self.value = value

    def test(self, value):
        return self.value == value


class MatchSuccess(Match):
    def test(self, value):
        return not isinstance(value, Exception)


class MatchError(Match):
    def test(self, value):
        return isinstance(value, Exception)


def parse_match(data: Dict[str, Any]) -> Match:
    data = dict(data)
    return globals()['Match' + data.pop("type").capitalize()].parse(data)


def parse_matches(items) -> Iterator[Match]:
    return map(parse_match, items)


class Rule(ABC):
    def __init__(self, matches: List[Match], name: Optional[str] = None):
        self.matches = matches
        self.name = name

    def applies(self, value) -> Iterator[Apply]:
        for match in self.matches:
            if match.test(value):
                yield from match.applies

    @abstractmethod
    def get_value(self, *, now: Datetime, flags: Dict[str, Any]) -> Any:
        pass

    @classmethod
    def parse(cls, data: dict) -> "Rule":
        data = dict(data)
        data["matches"] = parse_matches(data["matches"])
        return cls(**data)


class RuleUrl(Rule):
    def __init__(self, url: str, matches: List[Match], name=None):
        super().__init__(matches, name)
        self.url = url

    def get_value(self, **_):
        try:
            return requests.get(self.url).json()
        except Exception as e:
            logging.error(e)
            return e


class RulePeriods(Rule):
    def __init__(self, periods: List[TimePeriod], matches, name=None):
        super().__init__(matches, name)
        self.periods = periods

    def get_value(self, *, now: Datetime, **_):
        return any(now in p for p in self.periods)

    @classmethod
    def parse(cls, data: dict) -> "RulePeriods":
        data = dict(data)
        data["periods"] = parse_time_periods(data["periods"])
        return super().parse(data)

class RuleFlag(Rule):
    def __init__(self, flag: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flag = flag

    def get_value(self, *, flags, **_):
        return flags[self.flag]


def parse_rule(data: dict) -> Rule:
    data = dict(data)
    return globals()['Rule' + data.pop("type").capitalize()].parse(data)


def parse_rules(items) -> Iterator[Rule]:
    return map(parse_rule, items)
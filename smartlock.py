#!/usr/bin/env python3.8
"""
Usage:
    smartlock <config_file> [-A=ACTION] [--dry-run] [-R] [--time=TIME] [options]

Options:
    -s --dry-run
    -t --time=TIME
    -R --remote-time
    -A --action=ACTION
    -L --list-actions
    -P --positive-activity
    -l --log-level=LEVEL
"""
from typing import *
from utils.executor import Executor
from utils.action import Action, compute_actions
from utils.config import Config
from utils.remote_time import get_remote_utc_datetime
from docopt import docopt
import datetime as dt
import os
import logging
import yaml
import requests


def check_activity_positive(url: Optional[str]) -> Optional[bool]:
    if not url:
        return None
    try:
        return requests.get(url).json()
    except:
        return False


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


def main(args):
    logging.basicConfig(level=getattr(logging, args["--log-level"] or "INFO"))

    config = Config.parse_file(args["<config_file>"])
    env = {**os.environ, **config.env, "SMARTLOCK_PATH": os.path.dirname(os.path.abspath(__file__))}
    exe = Executor(config.shell, encoding=config.shell_encoding, dry_run=args["--dry-run"], env=env)

    now = get_now(config.timezone, use_remote=args["--remote-time"], parse_time=args["--time"])
    logging.debug("Now is %s" % now)

    if args["--action"]:
        exe.print_exec(config.commands[args["--action"]])
        return

    if args["--positive-activity"]:
        is_activity_positive = None
    else:
        is_activity_positive = check_activity_positive(config.is_activity_allowed_url)

    actions = compute_actions(
        now,
        is_activity_positive=is_activity_positive,
        allowed_activity_periods=config.allowed_activity_periods,
        danger_periods=config.danger_periods,
        critical_periods=config.critical_periods,
        allow_all_periods=config.allow_all_periods,
        dinner_periods=config.dinner_periods,
    )
    logging.debug(" ".join(action.name for action in actions))

    if args["--list-actions"]:
        print("\n".join(action.name for action in actions))
        return

    for action in actions:
        exe.print_exec(config.commands[action.name])


if __name__ == "__main__":
    main(docopt(__doc__))

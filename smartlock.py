#!/usr/bin/env python3.8
"""
Usage:
    smartlock [-A=ACTION] [--dry-run] [-R] [--time=TIME] [options]

Options:
    -C --config=FILE    Stdin is used by default
    -s --dry-run
    -t --time=TIME
    -R --remote-time
    -A --action=ACTION
    -L --list-actions
    -l --log-level=LEVEL
"""
from typing import *
from utils.executor import Executor
from utils.action import compute_actions
from utils.config import Config
from utils.now import get_now
from docopt import docopt
import datetime as dt
import os
import logging
import yaml
import requests
import sys


def read_config(path: Optional[str]) -> Config:
    if path:
        file = open(path)
    else:
        file = sys.stdin

    config = Config.parse(yaml.safe_load(file.read()))
    file.close()
    return config


def main(args):
    logging.basicConfig(level=getattr(logging, args["--log-level"] or "INFO"))
        
    config = read_config(args.get("--config"))
    env = {**os.environ, **config.global_env, **config.env, "SMARTLOCK_PATH": os.path.dirname(os.path.abspath(__file__))}
    exe = Executor(config.shell, encoding=config.shell_encoding, dry_run=args["--dry-run"], env=env)

    now = get_now(config.timezone, use_remote=args["--remote-time"], parse_time=args["--time"])
    logging.debug("Now is %s" % now)

    if args["--action"]:
        exe.print_exec(config.actions[args["--action"]])
        return

    try:
        actions = list(compute_actions(
            now=now,
            flags=config.flags,
            rules=config.rules,
        ))
    except Exception as e:
        logging.error("FAILSAFE")
        exe.print_exec(config.actions['FAILSAFE'])
        raise e

    if args["--list-actions"]:
        print("\n".join(actions))
        return

    for action in actions:
        exe.print_exec(config.actions[action])


if __name__ == "__main__":
    main(docopt(__doc__))

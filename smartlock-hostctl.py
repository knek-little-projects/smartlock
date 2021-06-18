#!/usr/bin/env python3.8
"""
Usage:
    hostctl block <path>
    hostctl unblock-marked <path>

Example:
    echo qwe.ru | hostctl block /etc/hosts
"""
from utils.hostsfile import HostsFile
from docopt import docopt
import sys

if __name__ == "__main__":
    args = docopt(__doc__)

    hf = HostsFile(args["<path>"])

    if args["block"]:
        hosts = sys.stdin.read().split()
        hf.block(hosts)

    elif args["unblock-marked"]:
        hf.unblock_marked()

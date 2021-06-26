#!python3.8
from typing import *
from psutil import Process
from utils.headhash import headhash
import psutil
import logging
import subprocess


def ps_info(exe, prop) -> bytes:
    cmd = '''[System.Diagnostics.FileVersionInfo]::GetVersionInfo("%s").%s''' % (exe, prop)
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed.stdout


def _transform_user_name(s):
    s = s.strip()

    if '\\' in s:
        s = s.split('\\')[-1]

    return s.lower()


def is_user_eq(a, b):
    return _transform_user_name(a) == _transform_user_name(b)


def ps_bw_filter(
        user: str,
        path_wl: List[str], 
        name_bl: List[str],
        cname_bl: List[str],
        hash_bl: List[str],
    ) -> Iterator[Process]:

    path_wl = {path.strip().lower() for path in path_wl}
    name_bl = {name.strip().lower() for name in name_bl}
    cname_bl = {cname.strip().encode() for cname in cname_bl}

    for p in psutil.pids():
        try:
            p = Process(p)

            if not is_user_eq(p.username(), user):
                continue

            if not p.exe():
                continue

            if p.exe().lower() in path_wl:
                continue

            if p.name().lower() in name_bl:
                yield p
                continue

            if headhash(p.exe()) in hash_bl:
                yield p
                continue

            cname = ps_info(p.exe(), 'CompanyName').strip()
            if cname in cname_bl:
                yield p
                continue

        except psutil.AccessDenied:
            continue

        except psutil.NoSuchProcess:
            continue

        except OSError:
            continue


def killall(processes: Iterator[Process]):
    for p in processes:
        try:
            print("KILL", p.exe())
            p.kill()
        except Exception as e:
            logging.error(e)
            continue
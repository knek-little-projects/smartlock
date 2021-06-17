#!python3.8
from typing import *
import psutil
import logging
import subprocess


def ps_info(exe, prop) -> bytes:
    cmd = '''[System.Diagnostics.FileVersionInfo]::GetVersionInfo("%s").%s''' % (exe, prop)
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed.stdout

def ps_filter(exe_path_wl: List[str], exe_cname_wl: List[str]) -> Iterator[psutil.Process]:
    allow_instances = {exe.strip() for exe in exe_path_wl if exe}
    allow_companies = {cname.strip().encode() for cname in exe_cname_wl if cname}

    for p in psutil.pids():
        try:
            p = psutil.Process(p)
            logging.debug("PSUTIL %s" % p.exe())

            if p.username() != 'qwe-ПК\\qwe':
                logging.debug("PSUTIL SKIP Username outside of scope")
                continue

            if p.exe() in allow_instances:
                logging.debug("PSUTIL SKIP Allowed instance")
                continue

            if not p.exe():
                logging.debug("PSUTIL SKIP None exe")
                continue

            cname = ps_info(p.exe(), 'CompanyName')
            if any(allowed_substr in cname for allowed_substr in allow_companies):
                logging.debug("PSUTIL SKIP Allowed cname: %s" % cname)
                continue

            logging.info("MATCH %s" % p.exe())
            yield p

        except psutil.AccessDenied:
            continue

        except psutil.NoSuchProcess:
            continue

        except OSError:
            continue

def ps_filter_kill(*args):
    for p in ps_filter(*args):
        p.kill()
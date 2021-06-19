import sys
import os
sys.path.insert(0, os.environ["SMARTLOCK_PATH"])

from utils.hostsfile import HostsFile
LIST = os.environ['disallow_hosts'].splitlines()
PATH = r"C:\Windows\System32\drivers\etc\hosts"
HostsFile(PATH).block(LIST)

from utils.ps import ps_filter_wl, ps_filter_by, killall
PATH = os.environ['exe_path_whitelist'].splitlines()
CNAME = os.environ['exe_cname_whitelist'].splitlines()
killall(ps_filter_wl(PATH, CNAME))

UNLOCK_FLAG = os.environ["unlock_activities_flag"]
if os.path.isfile(UNLOCK_FLAG):
    os.unlink(UNLOCK_FLAG)
    killall(ps_filter_by("chrome.exe"))
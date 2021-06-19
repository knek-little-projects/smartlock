import sys
import os
sys.path.insert(0, os.environ["SMARTLOCK_PATH"])

from utils.hostsfile import HostsFile
LIST = os.environ['disallow_hosts'].splitlines()
PATH = r"C:\Windows\System32\drivers\etc\hosts"
HostsFile(PATH).block(LIST)

from utils.ps import ps_filter_kill
PATH = os.environ['exe_path_whitelist'].splitlines()
CNAME = os.environ['exe_cname_whitelist'].splitlines()
ps_filter_kill(PATH, CNAME)

UNLOCK_FLAG = os.environ["unlock_activities_flag"]
if os.path.isfile(UNLOCK_FLAG):
    os.unlink(UNLOCK_FLAG)
    os.system("taskkill /IM chrome.exe")
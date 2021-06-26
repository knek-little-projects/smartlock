###################
# BLOCK /etc/hosts
###################

import sys
import os
sys.path.insert(0, os.environ["SMARTLOCK_PATH"])

from utils.hostsfile import HostsFile
LIST = os.environ['disallow_hosts'].splitlines()
PATH = r"C:\Windows\System32\drivers\etc\hosts"
HostsFile(PATH).block(LIST)

###################
# KILL PROCESSES
###################

from utils.ps import ps_bw_filter, killall

user = os.environ['user'].strip()
cname_bl = os.environ['cname_bl'].splitlines()
name_bl = os.environ['name_bl'].splitlines()
hash_bl = os.environ['hash_bl'].splitlines()
path_wl = os.environ['path_wl'].splitlines()

unlock_activities_flag = os.environ["unlock_activities_flag"]
if os.path.isfile(unlock_activities_flag):
    os.unlink(unlock_activities_flag)
    name_bl += os.environ['kill_on_activity_reblock'].splitlines()

killall(ps_bw_filter(
    user=user,
    path_wl=path_wl,
    name_bl=name_bl,
    cname_bl=cname_bl,
    hash_bl=hash_bl,
))
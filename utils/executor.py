from typing import *
import subprocess


class Executor:
    def __init__(self, dry_run: bool = False, env: Optional[Dict[str, str]] = None):
        self.dry_run = dry_run
        self.env = env

    def execute(self, cmd: str):
        """
        >>> e = Executor(dry_run=True, env=dict(user='x'))
        >>> retcode = e.execute("qwe $user")
        qwe x
        >>> retcode
        0
        >>> e = Executor(dry_run=False, env=dict(user='x'))
        >>> e.execute("echo qwe $user")
        0
        >>>  
        """
        env = self.env or {}

        if self.dry_run:

            for key, val in env.items():
                cmd = cmd.replace("$%s" % key, val)

            print(cmd)
            return 0

        else:
            return subprocess.call(cmd, shell=True, env=env)

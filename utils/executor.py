from typing import *
from subprocess import Popen, PIPE, STDOUT
import subprocess
import os


class Executor:
    def __init__(self, shell, *, dry_run: bool = False, env: Optional[Dict[str, str]] = None, encoding="UTF-8"):
        self.shell = shell
        self.dry_run = dry_run
        self.env = env or {}
        self.encoding = encoding

    def execute(self, input: bytes) -> bytes:
        if self.dry_run:
            return input

        env = self.env or {}

        p = Popen(self.shell, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, env=env)
        p.stdin.write(input)
        p.stdin.write(b'\n')
        output, _ = p.communicate()
        
        return output

    def print_exec(self, cmd: str):
        """
        >>> e = Executor("/bin/sh", dry_run=False, env={"user": "qwerty"})
        >>> e.print_exec("echo 1\\necho 2\\necho $user")
        1
        2
        qwerty
        <BLANKLINE>
        >>> e.dry_run = True
        >>> e.print_exec("echo 1\\necho 2\\necho 3")
        echo 1
        echo 2
        echo 3
        >>> 
        """
        print(self.execute(cmd.encode(self.encoding)).decode(self.encoding))

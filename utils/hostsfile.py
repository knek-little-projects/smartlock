from typing import *


class HostsFile:
    """
    >>> import os
    >>> FILE = "/tmp/hosts"
    >>> hf = HostsFile(FILE)
    >>> hf.write("127.0.0.1 qwe")
    >>> print(hf.read())
    127.0.0.1 qwe
    >>> hf.block(["asd"])
    >>> print(hf.read())
    127.0.0.1 qwe
    0.0.0.0 asd # SMARTLOCK
    >>> hf.unblock_marked()
    >>> print(hf.read())
    127.0.0.1 qwe
    >>> os.unlink(FILE)
    """

    def __init__(self, path, redirect="0.0.0.0", mark="SMARTLOCK"):
        self._path = path
        self._mark = mark
        self._redirect = redirect
        self._comment = "#"

    def read(self) -> str:
        with open(self._path) as input:
            return input.read()

    def write(self, text: str):
        with open(self._path, "w") as output:
            output.write(text)

    def _new_lines(self, hosts: List[str]) -> Iterator[str]:
        for host in hosts:
            yield " ".join((self._redirect, host, self._comment, self._mark))

    def _marked_lines(self, lines: List[str]) -> Iterator[str]:
        mark = "%s %s" % (self._comment, self._mark)
        for line in lines:
            if mark in line:
                yield line

    def block(self, hosts: List[str]):
        old_lines = self.read().splitlines()
        new_lines = list(set(self._new_lines(hosts)) - set(old_lines))
        self.write("\n".join(old_lines + new_lines))

    def unblock_marked(self):
        old_lines = self.read().splitlines()
        del_lines = set(self._marked_lines(old_lines))
        self.write("\n".join(line for line in old_lines if line not in del_lines))


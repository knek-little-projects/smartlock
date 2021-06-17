from typing import *
from datetime import time as Time
from datetime import datetime as Datetime
import requests

from utils.action import Action


class API:
    """
    >>> TEST_ADDRESS = "http://127.0.0.1:12345/"

    >>> api = API("UNAUTHORIZED", TEST_ADDRESS)
    >>> api.is_logged_in()
    False

    >>> api = API("TEST", ADDRESS)
    >>> api.is_logged_in()
    True

    >>> type(api.get_time())
    <class 'datetime.time'>
    
    >>> old_balance = api.get_balance()
    >>> api.add_balance(10) - old_balance
    10

    >>> api.add_balance(-10) - old_balance
    0

    >>> api.set_balance(10)
    >>> api.spend_balance(10)
    True
    
    >>> api.spend_balance(1)
    False
    >>> 
    """

    def __init__(self, api_key: str, address_prefix: str):
        self._address_prefix = address_prefix
        self._api_key = api_key

    def _get_auth_headers(self) -> Dict[str, str]:
        return {"API_KEY": self._api_key}

    def is_logged_in(self) -> bool:
        return self._get("login")

    def get_time(self) -> Time:
        return Datetime.strptime(self._get("time"), "%H:%M").time()

    def get_balance(self) -> int:
        return self._get("balance")

    def set_balance(self, value: int) -> int:
        return self._post("balance", value=value)

    def spend_balance(self, value: int) -> bool:
        return self._post("spend", value=value)

    def add_balance(self, value: int) -> int:
        return self._post("balance/add", value=value)

    def _post(self, relpath, **json) -> Any:
        return requests.post(self._address_prefix + relpath, headers=self._get_auth_headers(), json=json).json()

    def _get(self, relpath) -> Any:
        return requests.get(self._address_prefix + relpath, headers=self._get_auth_headers()).json()

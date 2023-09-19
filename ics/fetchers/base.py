from abc import ABC, abstractmethod
from typing import Any, Mapping, Collection

import httpx

from ..events import Event


class Fetcher(ABC):
    @abstractmethod
    async def fetch(self, client: httpx.AsyncClient) -> Collection[Event]:
        raise NotImplementedError()

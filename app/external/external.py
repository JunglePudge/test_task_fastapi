from abc import ABC, abstractmethod
from typing import List


class AbstractExternal(ABC):
    @abstractmethod
    def get_items(self, page: int, limit: int, since: str | None) -> List[dict]:
        pass
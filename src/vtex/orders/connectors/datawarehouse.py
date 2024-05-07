from abc import ABC, abstractmethod
from typing import List, Any

class DataWareHouse(ABC):
    @abstractmethod
    def insert_rows(self, table: str, data: List[dict], **configuration: dict) -> dict:
        ...
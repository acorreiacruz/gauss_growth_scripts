from ..connectors.datawarehouse import DataWareHouse
from typing import List


class Load:
    def __init__(self, datawarehouse: DataWareHouse) -> None:
        self.datawarehouse: DataWareHouse = datawarehouse

    def run(self,table: str, data: List[dict]) -> dict:
        result = self.datawarehouse.insert_rows(table=table, data=data)
        return result
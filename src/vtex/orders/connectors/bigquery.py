from typing import Any, List
from google.cloud.bigquery import Client
from .datawarehouse import DataWareHouse


class BigQueryConnector(DataWareHouse):
    def __init__(self) -> None:
        super().__init__()
        self.client: Client = Client()
    def insert_rows(self, table: str, data: List[dict], **configuration: dict) -> dict:
        result = self.client.insert_rows(table=table, rows=data, **configuration)
        return {"success": "All data inserted"} if not result else {"error": result}
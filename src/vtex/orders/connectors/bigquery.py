from google.cloud.bigquery import Client


class BigQueryConnector:
    def __init__(self) -> None:
        self.client = Client()

    def insert_rows(self, table: str, data: list, **kwargs) -> list:
        results = self.client.insert_rows_json(table=table, json_rows=data, **kwargs)
        return results

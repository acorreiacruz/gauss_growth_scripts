from flask import Request
from flask.typing import ResponseReturnValue
from functions_framework import http
from .connectors.vtex import VtexAPIConnector
from .utils import DateTimeConfig
from .utils import Formatter

class LoadOrdersData(DateTimeConfig):
    def __init__(self) -> None:
        self.vtex_api: VtexAPIConnector = VtexAPIConnector()
        super().__init__()
        self.YESTERDAY_START_STR = Formatter.string_from_datetime(
            self.YESTERDAY_UTC_START
        )
        self.YESTERDAY_END_STR = Formatter.string_from_datetime(
            self.YESTERDAY_UTC_END
        )

    def get_orders(self) -> list:
        params = {
            "orderBy": "creationDate,asc",
            "f_creationDate": f"creationDate:[{self.YESTERDAY_START_STR}Z TO {self.YESTERDAY_END_STR}Z]",
        }
        return self.vtex_api.consult_orders(params=params)

    def get_orders_ids(self, orders: list) -> list:
        return [order["orderId"] for order in orders]

    def get_detailed_orders(self, order_ids: list) -> list:
        orders = []
        for id in order_ids:
            vtex_order = self.vtex_api.detail_order(order_id=id)
            orders.append(vtex_order)
        return orders

    def formmat_records(self, orders: list) -> list:
        formmated_records = {}
        for order in orders:
            ...

    def insert_record_in_db(self, records: dict) -> None:
        self.client.insert_rows_from_dataframe()

    def main(self) -> list:
        print(f"Obtendo os dados de pedidos em: {self.YESTERDAY_UTC_DATE} ...")
        yesterday_vtex_orders = self.get_orders()
        if not yesterday_vtex_orders:
            exit(1)
        print(
            f"Número de pedidos em {self.YESTERDAY_UTC_DATE}: {len(yesterday_vtex_orders)}"
        )
        vtex_orders_ids = self.get_orders_ids(orders=yesterday_vtex_orders)
        print("Obtendo os pedidos de forma detalhada ...")
        orders = self.get_detailed_orders(order_ids=vtex_orders_ids)
        return orders


@http
def run(request: Request) -> ResponseReturnValue:
    orders = LoadOrdersData().main()
    return orders

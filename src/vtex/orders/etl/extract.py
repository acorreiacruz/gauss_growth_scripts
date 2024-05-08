from typing import List

from ..connectors import VtexAPIConnector
from ..utils import DateTimeConfig, Formatter


class Extract(DateTimeConfig):
    def __init__(self) -> None:
        super().__init__()
        self.vtex_api: VtexAPIConnector = VtexAPIConnector()
        self.YESTERDAY_START_STR = Formatter.string_from_datetime(
            self.YESTERDAY_UTC_START
        )
        self.YESTERDAY_END_STR = Formatter.string_from_datetime(self.YESTERDAY_UTC_END)

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

    def run(self) -> List[dict]:
        print(
            f"Obtendo os dados de pedidos entre {self.YESTERDAY_START_STR} e {self.YESTERDAY_END_STR}"
        )
        yesterday_vtex_orders = self.get_orders()
        if not yesterday_vtex_orders:
            return []
        print(f"Número de pedidos {len(yesterday_vtex_orders)}")
        vtex_orders_ids = self.get_orders_ids(orders=yesterday_vtex_orders)
        print("Obtendo os pedidos de forma detalhada ...")
        orders = self.get_detailed_orders(order_ids=vtex_orders_ids)
        return orders

from math import ceil

import requests

from src.vtex.orders.settings import VTEX_API_HOST, VTEX_KEY, VTEX_TOKEN


class VtexAPIConnector:
    def __init__(
        self,
        host: str = VTEX_API_HOST,
        key: str = VTEX_KEY,
        token: str = VTEX_TOKEN,
    ) -> None:
        self.host = host
        self.key = key
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-VTEX-API-AppKey": self.key,
            "X-VTEX-API-AppToken": self.token,
        }

    def consult_orders(self, params: dict) -> list:
        endpoint = f"{self.host}/oms/pvt/orders/"
        params["page"] = 1
        params["per_page"] = 100
        response = requests.get(url=endpoint, headers=self.headers, params=params)
        response.raise_for_status()
        response = response.json()
        orders = response["list"]
        total_pages = ceil(response["paging"]["total"] / params["per_page"])
        while params["page"] < total_pages:
            params["page"] += 1
            response = requests.get(url=endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            response = response.json()
            orders.extend(response["list"])
        return orders

    def detail_order(self, order_id: str) -> dict:
        endpoint = f"{self.host}/oms/pvt/orders/{order_id}/"
        response = requests.get(url=endpoint, headers=self.headers)
        response = response.json()
        return response

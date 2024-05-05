from flask import Request
from flask.typing import ResponseReturnValue
from functions_framework import http

from .connectors.bigquery import BigQueryConnector
from .connectors.vtex import VtexAPIConnector
from .utils import DateTimeConfig, Formatter


class LoadOrdersData(DateTimeConfig):
    def __init__(self) -> None:
        super().__init__()
        self.db_client = BigQueryConnector()
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

    def get_order_totals(self, order: dict) -> dict:
        totals = order.get("totals")
        return (
            {total.get("id"): total.get("value") for total in totals} if totals else {}
        )

    def get_clients_emails(self) -> dict: ...

    def formmat_records(self, orders: list) -> list:
        formmated_records = []
        for order in orders:
            creation_date = Formatter.convert_utc_str_to_timezone(
                value=order.get("creationDate")
            )
            totals = self.get_order_totals(order=order)
            formmated_records.append(
                {
                    "date": Formatter.string_from_datetime(creation_date),
                    "period": (
                        "morning"
                        if 5 <= creation_date.hour < 12
                        else "afternoon" if 12 <= creation_date.hour < 18 else "night"
                    ),
                    "id": order.get("orderId"),
                    "status": order.get("status"),
                    "status_description": order.get("statusDescription"),
                    "client_id": order.get("clientProfileData", {}).get(
                        "userProfileId"
                    ),
                    "client_name": f"{order.get('clientProfileData', {}).get('firstName')} {order.get('clientProfileData', {}).get('lastName')}".title(),
                    "email": order.get("clientProfileData", {}).get("email"),
                    "phone": Formatter.clean_phone(
                        order.get("clientProfileData", {}).get("phone", "")
                    ),
                    "birthdate": None,  # Não fornecido nos dados
                    "age": None,  # Não fornecido nos dados
                    "cpf_cnpj": Formatter.clean_cpf_cnpj(
                        order.get("clientProfileData", {}).get("document", "")
                    ),
                    "shipping": order.get("shippingData", {})
                    .get("logisticsInfo", [{}])[0]
                    .get("deliveryCompany"),
                    "shipping_value": totals.get("Shipping", 0) / 100,
                    "subtotal": totals.get("Items", 0) / 100,
                    "discount": totals.get("Discounts", 0) / 100,
                    "additional": None,  # Não fornecido nos dados
                    "total": order.get("value", 0) / 100,
                    "items_count": len(order.get("items", [])),
                    "payment_status": None,  # Não fornecido nos dados
                    "payment_service": order.get("paymentData", {})
                    .get("transactions", [{}])[0]
                    .get("payments", [{}])[0]
                    .get("connectorResponses", {})
                    .get("acquirer"),
                    "payment_type": order.get("paymentData", {})
                    .get("transactions", [{}])[0]
                    .get("payments", [{}])[0]
                    .get("group"),
                    "installments": order.get("paymentData", {})
                    .get("transactions", [{}])[0]
                    .get("payments", [{}])[0]
                    .get("installments"),
                    "seller_id": order.get("sellers", [{}])[0].get("id"),
                    "seller": order.get("sellers", [{}])[0].get("name"),
                    "store": order.get("marketplace", {}).get("name"),
                    "coupon_id": None,  # Não fornecido nos dados
                    "coupon": order.get("marketingData", {}).get("coupon"),
                    "table_id": None,  # Não fornecido nos dados
                    "table_name": None,  # Não fornecido nos dados
                    "address": order.get("shippingData", {})
                    .get("address", {})
                    .get("street"),
                    "address_number": order.get("shippingData", {})
                    .get("address", {})
                    .get("number"),
                    "address_complement": order.get("shippingData", {})
                    .get("address", {})
                    .get("complement"),
                    "neighborhood": order.get("shippingData", {})
                    .get("address", {})
                    .get("neighborhood"),
                    "city": order.get("shippingData", {})
                    .get("address", {})
                    .get("city"),
                    "state": order.get("shippingData", {})
                    .get("address", {})
                    .get("state"),
                    "postal_code": order.get("shippingData", {})
                    .get("address", {})
                    .get("postalCode"),
                }
            )
        return formmated_records

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
        print("Formatando os registros para inserir ...")
        formatted_records = self.formmat_records(orders=orders)
        print("Inserindo os registros na tabela Orders Consolidated do dataset Vtex")
        result = self.db_client.insert_rows(
            table="gaussgrowth.vtex.orders_consolidated", data=formatted_records
        )
        return result


@http
def run(request: Request) -> ResponseReturnValue:
    result = LoadOrdersData().main()
    return (
        {"errors": result}
        if result
        else {"success": "Os dados foram inseridos com sucesso"}
    )

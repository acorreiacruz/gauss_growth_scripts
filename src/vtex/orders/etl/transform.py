from ..utils import Formatter
from typing import List


class Transform:

    def __get_order_totals(self, order: dict) -> dict:
        totals = order.get("totals")
        return (
            {total.get("id"): total.get("value") for total in totals} if totals else {}
        )

    def run(self, orders: List[dict]) -> List[dict]:
        formmated_records = []
        for order in orders:
            creation_date = Formatter.convert_utc_str_to_timezone(
                value=order.get("creationDate")
            )
            totals = self.__get_order_totals(order=order)
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
                    "client_id": (order.get("clientProfileData") or {}).get(
                        "userProfileId"
                    ),
                    "client_name": f"{(order.get('clientProfileData') or {}).get('firstName')} {(order.get('clientProfileData') or {}).get('lastName')}".title(),
                    "email": (order.get("clientProfileData") or {}).get("email"),
                    "phone": Formatter.clean_phone(
                        (order.get("clientProfileData") or {}).get("phone", "")
                    ),
                    "birthdate": None,
                    "age": None,
                    "cpf_cnpj": Formatter.clean_cpf_cnpj(
                        (order.get("clientProfileData") or {}).get("document", "")
                    ),
                    "shipping": (order.get("shippingData", {}) or {})
                    .get("logisticsInfo", [{}])[0]
                    .get("deliveryCompany"),
                    "shipping_value": totals.get("Shipping", 0) / 100,
                    "subtotal": totals.get("Items", 0) / 100,
                    "discount": totals.get("Discounts", 0) / 100,
                    "additional": None,
                    "total": order.get("value", 0) / 100,
                    "items_count": len(order.get("items", [])),
                    "payment_status": None,
                    "payment_service": (order.get("paymentData", {}) or {})
                    .get("transactions", [{}])[0]
                    .get("payments", [{}])[0]
                    .get("connectorResponses", {})
                    .get("acquirer"),
                    "payment_type": (order.get("paymentData", {}) or {})
                    .get("transactions", [{}])[0]
                    .get("payments", [{}])[0]
                    .get("group"),
                    "installments": (order.get("paymentData", {}) or {})
                    .get("transactions", [{}])[0]
                    .get("payments", [{}])[0]
                    .get("installments"),
                    "seller_id": (order.get("sellers", [{}])[0] or {}).get("id"),
                    "seller": (order.get("sellers", [{}])[0] or {}).get("name"),
                    "store": (order.get("marketplace") or {}).get("name"),
                    "coupon_id": None,
                    "coupon": (order.get("marketingData") or {}).get("coupon"),
                    "table_id": None,
                    "table_name": None,
                    "address": (order.get("shippingData", {}) or {})
                    .get("address", {})
                    .get("street"),
                    "address_number": (order.get("shippingData", {}) or {})
                    .get("address", {})
                    .get("number"),
                    "address_complement": (order.get("shippingData", {}) or {})
                    .get("address", {})
                    .get("complement"),
                    "neighborhood": (order.get("shippingData", {}) or {})
                    .get("address", {})
                    .get("neighborhood"),
                    "city": (order.get("shippingData", {}) or {})
                    .get("address", {})
                    .get("city"),
                    "state": (order.get("shippingData", {}) or {})
                    .get("address", {})
                    .get("state"),
                    "postal_code": (order.get("shippingData", {}) or {})
                    .get("address", {})
                    .get("postalCode"),
                }
            )
        return formmated_records

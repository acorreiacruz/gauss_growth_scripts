import functions_framework
from flask import Request, typing
from .connectors import BigQueryConnector
from .etl import Extract
from .etl import Load
from .etl import Transform

@functions_framework.http
def run_pipeline(request: Request) -> typing.ResponseReturnValue:
    orders = Extract().run()
    formmated_orders = Transform().run(orders=orders)
    bigquery = BigQueryConnector()
    result = Load(datawarehouse=bigquery).run(table="gaussgrowth.vtex.orders_consolidated", data=formmated_orders)
    return result
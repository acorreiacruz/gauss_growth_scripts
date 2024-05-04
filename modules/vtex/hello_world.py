from functions_framework import http
from flask import Request
from flask.typing import ResponseReturnValue

@http
def hello_world(request: Request) -> ResponseReturnValue:
    if request.method == "GET":
        return "Hello World !"
    raise Exception("HTTP method not allowed !")
import os
from dotenv import load_dotenv

load_dotenv()

# Vtex
VTEX_ACCOUNT_NAME = os.environ.get("VTEX_ACCOUNT_NAME")
VTEX_ENVIRONMENT = os.environ.get("VTEX_ENVIRONMENT")
VTEX_KEY = os.environ.get("VTEX_KEY")
VTEX_TOKEN = os.environ.get("VTEX_TOKEN")
VTEX_API_HOST = f"https://{VTEX_ACCOUNT_NAME}.{VTEX_ENVIRONMENT}.com.br/api"


import os
from dotenv import load_dotenv
import logging

load_dotenv()

COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
COGNITO_APP_CLIENT_SECRET = os.getenv("COGNITO_APP_CLIENT_SECRET")

required_vars = [
    "COGNITO_USER_POOL_ID",
    "COGNITO_APP_CLIENT_ID",
    "COGNITO_APP_CLIENT_SECRET",
]

for var in required_vars:
    if not globals()[var]:
        logging.critical(f"Environment variable {var} not set.")
        raise EnvironmentError(f"Environment variable {var} not set.")

import os
from dotenv import load_dotenv
import logging

load_dotenv()

COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
COGNITO_APP_CLIENT_SECRET = os.getenv("COGNITO_APP_CLIENT_SECRET")
COGNITO_KEYS_URL = f"https://cognito-idp.us-east-1.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
COGNITO_ISSUER = f"https://cognito-idp.us-east-1.amazonaws.com/{COGNITO_USER_POOL_ID}"
DYNAMO_MESSAGES_TABLE = os.getenv("DYNAMO_MESSAGES_TABLE")
CORS_ALLOWED_DOMAIN = os.getenv("CORS_ALLOWED_DOMAIN")
ENV = os.getenv("ENV", "develop")

required_vars = [
    "COGNITO_USER_POOL_ID",
    "COGNITO_APP_CLIENT_ID",
    "COGNITO_APP_CLIENT_SECRET",
    "COGNITO_KEYS_URL",
    "COGNITO_ISSUER",
    "DYNAMO_MESSAGES_TABLE",
    "CORS_ALLOWED_DOMAIN",
    "ENV",
]

for var in required_vars:
    if not globals()[var]:
        logging.critical(f"Environment variable {var} not set.")
        raise EnvironmentError(f"Environment variable {var} not set.")

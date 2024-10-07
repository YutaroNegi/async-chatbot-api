import hmac
import hashlib
import base64
import urllib.request
from functools import lru_cache
import json
from fastapi import HTTPException, status
import logging
from app import config

logger = logging.getLogger("app.utils.auth")


def get_secret_hash(username: str, client_id: str, client_secret: str) -> str:
    """
    Generates the SECRET_HASH required for AWS Cognito authentication.

    Args:
        username (str): The username (email) of the user.
        client_id (str): The Cognito App Client ID.
        client_secret (str): The Cognito App Client Secret.

    Returns:
        str: The computed SECRET_HASH.
    """
    logger.info("Generating SECRET_HASH")
    message = username + client_id
    dig = hmac.new(
        client_secret.encode("utf-8"),
        msg=message.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    logger.debug(f"SECRET_HASH: {dig}")
    return base64.b64encode(dig).decode()


@lru_cache()
def get_public_keys():
    try:
        logger.info("Fetching public keys")
        with urllib.request.urlopen(config.COGNITO_KEYS_URL) as f:
            response = f.read()
        keys = json.loads(response.decode("utf-8"))["keys"]
        logger.debug(f"Public keys: {keys}")
        return keys
    except Exception as e:
        logger.error(f"Error fetching public keys: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching public keys",
        )

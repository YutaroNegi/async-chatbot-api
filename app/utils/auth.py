import hmac
import hashlib
import base64


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
    message = username + client_id
    dig = hmac.new(
        client_secret.encode("utf-8"),
        msg=message.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    return base64.b64encode(dig).decode()

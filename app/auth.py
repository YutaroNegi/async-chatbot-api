import time
from app import config
from app.utils.auth import get_public_keys
from jose import jwk, jwt
from jose.utils import base64url_decode
from jose.exceptions import JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

logger = logging.getLogger("app.auth")
security = HTTPBearer()


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    logger.info("Authentication attempt initiated.")
    token = token.credentials
    logger.debug(f"Received token: {token}")

    try:
        headers = jwt.get_unverified_header(token)
        logger.debug(f"Token headers: {headers}")
    except JWTError as e:
        logger.error(f"JWTError during header extraction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token header. Use an appropriate JWT token.",
        )

    kid = headers.get("kid")
    if not kid:
        logger.warning("Token header missing 'kid' field.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token header. 'kid' field missing.",
        )

    keys = get_public_keys()
    key_index = None

    for i, key in enumerate(keys):
        if kid == key["kid"]:
            key_index = i
            logger.debug(f"Matching key found: {key}")
            break

    if key_index is None:
        logger.warning(f"No matching public key found for kid: {kid}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Public key not found in jwks.json",
        )

    public_key = jwk.construct(keys[key_index])
    logger.debug(f"Public key constructed: {public_key}")

    try:
        message, encoded_signature = str(token).rsplit(".", 1)
    except ValueError as e:
        logger.error(f"Error splitting token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token structure.",
        )

    try:
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
        logger.debug(f"Decoded signature: {decoded_signature}")
    except Exception as e:
        logger.error(f"Error decoding signature: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature encoding.",
        )

    if not public_key.verify(message.encode("utf-8"), decoded_signature):
        logger.warning("Signature verification failed.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature verification failed",
        )
    logger.info("Signature verification succeeded.")

    try:
        claims = jwt.get_unverified_claims(token)
        logger.debug(f"Token claims: {claims}")
    except JWTError as e:
        logger.error(f"JWTError during claims extraction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token claims.",
        )

    current_time = time.time()
    if current_time > claims.get("exp", 0):
        logger.warning("Token is expired.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is expired",
        )

    if claims.get("iss") != config.COGNITO_ISSUER:
        logger.warning(f"Invalid issuer: {claims.get('iss')}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid issuer",
        )

    if claims.get("token_use") != "access":
        logger.warning(f"Invalid token use: {claims.get('token_use')}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token use",
        )

    if claims.get("client_id") != config.COGNITO_APP_CLIENT_ID:
        logger.warning(f"Invalid client ID: {claims.get('client_id')}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client ID",
        )

    logger.info(f"User authenticated successfully: {claims.get('username')}")
    return claims

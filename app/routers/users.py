from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from app.models.users import User, UserCreate, UserLogin
from app.utils.auth import get_secret_hash
from app.auth import get_current_user
import os
import boto3
from botocore.exceptions import ClientError
import logging
from app import config

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

logger = logging.getLogger("app.routers.users")

cognito_client = boto3.client("cognito-idp")
USER_POOL_ID = config.COGNITO_USER_POOL_ID
CLIENT_ID = config.COGNITO_APP_CLIENT_ID
CLIENT_SECRET = config.COGNITO_APP_CLIENT_SECRET
IS_PRODUCTION = config.ENV == "production"


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    logger.info(f"Registration attempt for email: {user.email}")
    try:
        _ = cognito_client.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=user.email,
            UserAttributes=[
                {"Name": "email", "Value": user.email},
                {"Name": "email_verified", "Value": "true"},
            ],
            TemporaryPassword=user.password,
            MessageAction="SUPPRESS",
        )
        logger.info(f"User {user.email} created successfully in Cognito.")

        cognito_client.admin_set_user_password(
            UserPoolId=USER_POOL_ID,
            Username=user.email,
            Password=user.password,
            Permanent=True,
        )

        logger.info(f"User {user.email} created successfully in Cognito.")

        return {"message": "User created successfully"}
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        logger.error(
            f"Error creating user {user.email}: {e.response['Error']['Message']}"
        )

        if error_code == "UsernameExistsException":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        elif error_code == "InvalidParameterException":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid parameters provided",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )
    except Exception as e:
        logger.exception(
            f"Unexpected error during registration for {user.email}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user: UserLogin):
    logger.info(f"Login attempt for email: {user.email}")
    secret_hash = get_secret_hash(user.email, CLIENT_ID, CLIENT_SECRET)
    try:
        response = cognito_client.initiate_auth(
            ClientId=os.getenv("COGNITO_APP_CLIENT_ID"),
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": user.email,
                "PASSWORD": user.password,
                "SECRET_HASH": secret_hash,
            },
        )
        logger.info(f"User {user.email} authenticated successfully.")

        access_token = response["AuthenticationResult"]["AccessToken"]
        refresh_token = response["AuthenticationResult"]["RefreshToken"]
        expires_in = response["AuthenticationResult"]["ExpiresIn"]

        res = JSONResponse(content={"message": "Login successful"})

        res.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=IS_PRODUCTION,
            samesite="None" if IS_PRODUCTION else "Lax",
            max_age=expires_in,
            expires=expires_in,
            path="/",
        )
        res.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=IS_PRODUCTION,
            samesite="None" if IS_PRODUCTION else "Lax",
            max_age=30 * 24 * 60 * 60,
            expires=30 * 24 * 60 * 60,
            path="/",
        )

        return res

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        logger.error(
            f"Error authenticating user {user.email}: {e.response['Error']['Message']}"
        )

        if error_code in ["NotAuthorizedException", "UserNotFoundException"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )
    except Exception as e:
        logger.exception(f"Unexpected error during login for {user.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    res = JSONResponse(content={"message": "Logout successful"})
    res.delete_cookie(key="access_token", path="/")
    res.delete_cookie(key="refresh_token", path="/")
    return res


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.sub}

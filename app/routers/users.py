from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator
import os
import boto3
from botocore.exceptions import ClientError
import re
import logging

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

logger = logging.getLogger("app.routers.users")


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def password_policy(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v


cognito_client = boto3.client("cognito-idp")
USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    logger.info(f"Using user pool ID: {USER_POOL_ID}")

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

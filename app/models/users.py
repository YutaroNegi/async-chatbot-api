from pydantic import BaseModel, EmailStr, field_validator
import re
from typing import Optional


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


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    sub: str
    iss: str
    client_id: str
    origin_jti: Optional[str] = None
    event_id: Optional[str] = None
    token_use: str
    scope: Optional[str] = None
    auth_time: Optional[int] = None
    exp: int
    iat: int
    jti: str
    username: str

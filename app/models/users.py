from pydantic import BaseModel, EmailStr, field_validator
import re


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

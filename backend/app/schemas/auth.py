from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    timezone: str = "UTC"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    user_id: int
    email: str
    name: Optional[str]
    token: str


class LoginResponse(BaseModel):
    user_id: int
    token: str
    expires_at: datetime


class LogoutResponse(BaseModel):
    message: str


class ErrorDetail(BaseModel):
    field: Optional[str] = None
    issue: str


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Optional[ErrorDetail] = None

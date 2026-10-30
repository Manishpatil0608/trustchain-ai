from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Username or email address")
    password: str = Field(..., min_length=1, description="Password")


class UserResponse(BaseModel):
    id: str
    username: str
    email: Optional[str] = None
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class RefreshRequest(BaseModel):
    refresh_token: Optional[str] = Field(None, description="Refresh token string if not supplied via HttpOnly cookie")


class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_\-]+$")
    email: Optional[str] = Field(None, max_length=100)
    password: str = Field(..., min_length=8, max_length=128)
    role: str = Field(default="OPERATOR", pattern=r"^(ADMIN|OPERATOR|VIEWER)$")


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=128)


class UserStatusUpdateRequest(BaseModel):
    is_active: Optional[bool] = None
    role: Optional[str] = Field(None, pattern=r"^(ADMIN|OPERATOR|VIEWER)$")


class SecurityAuditEventResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    username: Optional[str] = None
    event_type: str
    details: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True

from typing import Optional, List, Callable
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from akta.vdr.database import get_db
from akta.auth import crud, security, schemas
from akta.vdr import models
from akta.logging import get_logger

logger = get_logger(__name__)

security_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    db: Session = Depends(get_db)
) -> models.UserModel:
    """
    FastAPI dependency to extract and authenticate the current application user.
    Supports Bearer token in Authorization header or access_token in cookies/headers.
    """
    token: Optional[str] = None

    if credentials and credentials.scheme.lower() == "bearer":
        token = credentials.credentials
    elif "access_token" in request.cookies:
        token = request.cookies.get("access_token")
    elif "X-Access-Token" in request.headers:
        token = request.headers.get("X-Access-Token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Missing Bearer token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        payload = security.decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload.")
        
        user = crud.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account no longer exists.")
        
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is disabled.")

        return user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_optional_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    db: Session = Depends(get_db)
) -> Optional[models.UserModel]:
    """Returns the current authenticated user if valid token present, otherwise None."""
    try:
        return get_current_user(request, credentials, db)
    except HTTPException:
        return None


def require_role(allowed_roles: List[str]) -> Callable:
    """
    Factory creating a FastAPI dependency enforcing server-side Role-Based Access Control (RBAC).
    Example: Depends(require_role(["ADMIN", "OPERATOR"]))
    """
    def role_checker(current_user: models.UserModel = Depends(get_current_user)) -> models.UserModel:
        normalized_roles = [r.upper() for r in allowed_roles]
        if current_user.role.upper() not in normalized_roles:
            logger.warning(
                f"Access denied for user '{current_user.username}' (role '{current_user.role}'). Required roles: {allowed_roles}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: Insufficient privileges. Required role: {', '.join(allowed_roles)}"
            )
        return current_user

    return role_checker

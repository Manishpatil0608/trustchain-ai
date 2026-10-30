from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, Body, Query
from sqlalchemy.orm import Session

from akta.config import settings
from akta.vdr.database import get_db
from akta.auth import schemas, crud, security
from akta.auth.dependencies import get_current_user, require_role
from akta.vdr import models
from akta.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication & Access Control"]
)


def get_client_ip(request: Request) -> str:
    """Safely extracts client IP address from request."""
    if request.headers.get("x-forwarded-for"):
        return request.headers.get("x-forwarded-for").split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"


@router.post("/login", response_model=schemas.TokenResponse)
async def login(
    req: schemas.LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Authenticates user credentials and issues short-lived access JWT and refresh token.
    Enforces account lockout (5 failed attempts -> 15 min lock).
    """
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("user-agent", "Unknown")

    try:
        user = crud.authenticate_user(
            db=db,
            username_or_email=req.username,
            password=req.password,
            client_ip=client_ip,
            user_agent=user_agent
        )

        access_token = security.create_access_token(user_id=user.id, username=user.username, role=user.role)
        refresh_token = crud.create_refresh_session(db=db, user_id=user.id, user_agent=user_agent, client_ip=client_ip)

        # Set HttpOnly cookie for refresh token for browser security
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,  # Set to True in HTTPS production
            samesite="lax",
            max_age=settings.refresh_token_expire_days * 86400
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.access_token_expire_minutes * 60
        )

        return schemas.TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
            user=schemas.UserResponse.from_orm(user)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/refresh", response_model=schemas.TokenResponse)
async def refresh_token(
    request: Request,
    response: Response,
    body: Optional[schemas.RefreshRequest] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Rotates refresh token and issues a new access token.
    Detects token reuse attacks and invalidates all user sessions upon violation.
    """
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("user-agent", "Unknown")

    # Extract refresh token from body or cookie
    rt_str: Optional[str] = None
    if body and body.refresh_token:
        rt_str = body.refresh_token
    elif "refresh_token" in request.cookies:
        rt_str = request.cookies.get("refresh_token")

    if not rt_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required in body or cookie."
        )

    try:
        new_refresh_token, user = crud.rotate_refresh_token(
            db=db,
            refresh_token_str=rt_str,
            user_agent=user_agent,
            client_ip=client_ip
        )

        new_access_token = security.create_access_token(user_id=user.id, username=user.username, role=user.role)

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.refresh_token_expire_days * 86400
        )
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.access_token_expire_minutes * 60
        )

        return schemas.TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
            user=schemas.UserResponse.from_orm(user)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    body: Optional[schemas.RefreshRequest] = Body(None),
    current_user: Optional[models.UserModel] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Invalidates the active refresh token session and clears authentication cookies.
    """
    rt_str = body.refresh_token if body and body.refresh_token else request.cookies.get("refresh_token")
    if rt_str:
        crud.revoke_refresh_session(db=db, refresh_token_str=rt_str, user_id=current_user.id if current_user else None)
    elif current_user:
        crud.revoke_all_user_sessions(db=db, user_id=current_user.id, reason="User explicit logout")

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"status": "success", "message": "Successfully logged out."}


@router.get("/me", response_model=schemas.UserResponse)
async def get_me(current_user: models.UserModel = Depends(get_current_user)):
    """Returns profile info for currently authenticated user."""
    return schemas.UserResponse.from_orm(current_user)


@router.post("/change-password")
async def change_password(
    req: schemas.PasswordChangeRequest,
    current_user: models.UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Securely updates password and revokes existing refresh tokens."""
    try:
        crud.change_user_password(
            db=db,
            user_id=current_user.id,
            current_password=req.current_password,
            new_password=req.new_password
        )
        return {"status": "success", "message": "Password changed successfully. Please log in again."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ==========================================
# Admin Management Endpoints
# ==========================================

@router.get("/users", response_model=List[schemas.UserResponse])
async def list_users(
    db: Session = Depends(get_db),
    admin: models.UserModel = Depends(require_role(["ADMIN"]))
):
    """Lists all application users (Admin only)."""
    users = db.query(models.UserModel).order_by(models.UserModel.created_at.desc()).all()
    return [schemas.UserResponse.from_orm(u) for u in users]


@router.post("/users", response_model=schemas.UserResponse)
async def create_user(
    req: schemas.UserCreateRequest,
    db: Session = Depends(get_db),
    admin: models.UserModel = Depends(require_role(["ADMIN"]))
):
    """Creates a new application user (Admin only)."""
    try:
        user = crud.create_user(
            db=db,
            username=req.username,
            password=req.password,
            email=req.email,
            role=req.role,
            is_active=True,
            created_by_admin=True
        )
        return schemas.UserResponse.from_orm(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/users/{user_id}/status", response_model=schemas.UserResponse)
async def update_user_status(
    user_id: str,
    req: schemas.UserStatusUpdateRequest,
    db: Session = Depends(get_db),
    admin: models.UserModel = Depends(require_role(["ADMIN"]))
):
    """Enables/disables account or changes role (Admin only)."""
    try:
        user = crud.update_user_status(db=db, user_id=user_id, is_active=req.is_active, role=req.role)
        return schemas.UserResponse.from_orm(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/users/{user_id}/revoke-sessions")
async def revoke_user_sessions(
    user_id: str,
    db: Session = Depends(get_db),
    admin: models.UserModel = Depends(require_role(["ADMIN"]))
):
    """Revokes all active refresh token sessions for a user (Admin only)."""
    crud.revoke_all_user_sessions(db=db, user_id=user_id, reason=f"Sessions revoked by admin '{admin.username}'")
    return {"status": "success", "message": f"All sessions for user ID '{user_id}' have been revoked."}


@router.get("/audit", response_model=List[schemas.SecurityAuditEventResponse])
async def list_security_audit_events(
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
    admin: models.UserModel = Depends(require_role(["ADMIN"]))
):
    """Lists security audit trail events (Admin only)."""
    events = db.query(models.SecurityAuditEventModel).order_by(models.SecurityAuditEventModel.timestamp.desc()).limit(limit).all()
    return [schemas.SecurityAuditEventResponse.from_orm(e) for e in events]

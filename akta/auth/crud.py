import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Tuple

from sqlalchemy.orm import Session

from akta.config import settings
from akta.logging import get_logger
from akta.vdr import models
from akta.auth.security import (
    hash_password,
    verify_password,
    hash_token,
    generate_refresh_token
)

logger = get_logger(__name__)


def log_security_audit_event(
    db: Session,
    user_id: Optional[str],
    username: Optional[str],
    event_type: str,
    details: Optional[str] = None,
    client_ip: Optional[str] = None,
    user_agent: Optional[str] = None
) -> models.SecurityAuditEventModel:
    """Logs a security audit record to the database."""
    audit_event = models.SecurityAuditEventModel(
        id=str(uuid.uuid4()),
        user_id=user_id,
        username=username,
        event_type=event_type,
        details=details,
        ip_address=client_ip,
        user_agent=user_agent,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(audit_event)
    try:
        db.commit()
        db.refresh(audit_event)
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to log security audit event: {e}")
    return audit_event


def get_user_by_id(db: Session, user_id: str) -> Optional[models.UserModel]:
    return db.query(models.UserModel).filter(models.UserModel.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.UserModel]:
    if not username:
        return None
    return db.query(models.UserModel).filter(models.UserModel.username.ilike(username.strip())).first()


def get_user_by_email(db: Session, email: Optional[str]) -> Optional[models.UserModel]:
    if not email:
        return None
    return db.query(models.UserModel).filter(models.UserModel.email.ilike(email.strip())).first()


def create_user(
    db: Session,
    username: str,
    password: str,
    email: Optional[str] = None,
    role: str = "OPERATOR",
    is_active: bool = True,
    created_by_admin: bool = False
) -> models.UserModel:
    """Creates a new user account with securely hashed password."""
    if get_user_by_username(db, username):
        raise ValueError(f"Username '{username}' is already taken.")
    if email and get_user_by_email(db, email):
        raise ValueError(f"Email '{email}' is already registered.")

    user_id = str(uuid.uuid4())
    hashed_pwd = hash_password(password)

    user = models.UserModel(
        id=user_id,
        username=username,
        email=email,
        password_hash=hashed_pwd,
        role=role.upper(),
        is_active=is_active,
        is_verified=True,
        failed_login_attempts=0,
        locked_until=None
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    log_security_audit_event(
        db=db,
        user_id=user.id,
        username=user.username,
        event_type="USER_CREATED",
        details=f"User account created with role '{user.role}' (Admin creation: {created_by_admin})"
    )
    return user


def authenticate_user(
    db: Session,
    username_or_email: str,
    password: str,
    client_ip: Optional[str] = None,
    user_agent: Optional[str] = None
) -> models.UserModel:
    """
    Authenticates user with username/email and password.
    Enforces account lockout policy (5 failed attempts -> 15 min lockout).
    Returns generic exception message to prevent username enumeration.
    """
    user = get_user_by_username(db, username_or_email)
    if not user:
        user = get_user_by_email(db, username_or_email)

    generic_error = "Invalid username or password"

    if not user:
        # Perform dummy verify to mitigate timing attacks
        verify_password(password, "$argon2id$v=19$m=65536,t=3,p=4$dummyhashdummyhash$dummyhashdummyhashdummyhash")
        log_security_audit_event(
            db=db, user_id=None, username=username_or_email,
            event_type="LOGIN_FAILED", details="User does not exist",
            client_ip=client_ip, user_agent=user_agent
        )
        raise ValueError(generic_error)

    now = datetime.now(timezone.utc)

    # Check if account is locked
    if user.locked_until:
        # Convert timezone if needed
        locked_until = user.locked_until
        if locked_until.tzinfo is None:
            locked_until = locked_until.replace(tzinfo=timezone.utc)

        if now < locked_until:
            remaining_mins = int((locked_until - now).total_seconds() / 60) + 1
            log_security_audit_event(
                db=db, user_id=user.id, username=user.username,
                event_type="LOGIN_DENIED_LOCKED",
                details=f"Account locked until {locked_until}. Remaining: {remaining_mins}m",
                client_ip=client_ip, user_agent=user_agent
            )
            raise ValueError(f"Account is temporarily locked. Try again in {remaining_mins} minutes.")

    # Verify password
    if not verify_password(password, user.password_hash):
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= settings.login_max_attempts:
            user.locked_until = now + timedelta(minutes=settings.login_lockout_minutes)
            db.commit()
            log_security_audit_event(
                db=db, user_id=user.id, username=user.username,
                event_type="LOCKOUT",
                details=f"Exceeded {settings.login_max_attempts} failed login attempts. Locked for {settings.login_lockout_minutes} mins.",
                client_ip=client_ip, user_agent=user_agent
            )
            raise ValueError(f"Account is temporarily locked due to multiple failed attempts.")

        db.commit()
        log_security_audit_event(
            db=db, user_id=user.id, username=user.username,
            event_type="LOGIN_FAILED",
            details=f"Failed attempt {user.failed_login_attempts}/{settings.login_max_attempts}",
            client_ip=client_ip, user_agent=user_agent
        )
        raise ValueError(generic_error)

    # Check if account is active
    if not user.is_active:
        log_security_audit_event(
            db=db, user_id=user.id, username=user.username,
            event_type="LOGIN_DENIED_DISABLED", details="Account is disabled",
            client_ip=client_ip, user_agent=user_agent
        )
        raise ValueError("Account is disabled. Contact system administrator.")

    # Login successful -> reset counters
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login_at = now
    db.commit()
    db.refresh(user)

    log_security_audit_event(
        db=db, user_id=user.id, username=user.username,
        event_type="LOGIN_SUCCESS", details="Successful login",
        client_ip=client_ip, user_agent=user_agent
    )
    return user


def create_refresh_session(
    db: Session,
    user_id: str,
    user_agent: Optional[str] = None,
    client_ip: Optional[str] = None
) -> str:
    """Creates a new refresh token session and stores hashed token in database."""
    token_str, jti = generate_refresh_token()
    token_hash_str = hash_token(token_str)
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=settings.refresh_token_expire_days)

    refresh_model = models.RefreshTokenModel(
        id=str(uuid.uuid4()),
        jti=jti,
        user_id=user_id,
        token_hash=token_hash_str,
        created_at=now,
        expires_at=expires_at,
        revoked_at=None,
        replaced_by=None,
        user_agent=user_agent,
        client_ip=client_ip
    )
    db.add(refresh_model)
    db.commit()
    return token_str


def rotate_refresh_token(
    db: Session,
    refresh_token_str: str,
    user_agent: Optional[str] = None,
    client_ip: Optional[str] = None
) -> Tuple[str, models.UserModel]:
    """
    Rotates a refresh token: invalidates current token, issues new token,
    and detects token reuse (revoking all sessions if reuse occurs).
    """
    token_hash_str = hash_token(refresh_token_str)
    token_entry = db.query(models.RefreshTokenModel).filter(models.RefreshTokenModel.token_hash == token_hash_str).first()

    if not token_entry:
        log_security_audit_event(
            db=db, user_id=None, username=None,
            event_type="REFRESH_FAILED", details="Invalid or unknown refresh token hash",
            client_ip=client_ip, user_agent=user_agent
        )
        raise ValueError("Invalid refresh token.")

    user = get_user_by_id(db, token_entry.user_id)
    if not user or not user.is_active:
        log_security_audit_event(
            db=db, user_id=token_entry.user_id, username=user.username if user else None,
            event_type="REFRESH_FAILED", details="User inactive or deleted",
            client_ip=client_ip, user_agent=user_agent
        )
        raise ValueError("Account is disabled or inactive.")

    now = datetime.now(timezone.utc)

    # Detect Refresh Token Reuse Attack
    if token_entry.revoked_at is not None:
        # Token reuse detected! Emergency security action: revoke ALL user sessions!
        revoke_all_user_sessions(db, user.id, reason="Refresh token reuse detected (security breach prevention)")
        log_security_audit_event(
            db=db, user_id=user.id, username=user.username,
            event_type="REUSE_DETECTED",
            details=f"Token JTI '{token_entry.jti}' was already revoked. All user sessions invalidated.",
            client_ip=client_ip, user_agent=user_agent
        )
        raise ValueError("Security violation: Token reuse detected. All sessions revoked.")

    # Check Expiration
    expires_at = token_entry.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if now > expires_at:
        token_entry.revoked_at = now
        db.commit()
        log_security_audit_event(
            db=db, user_id=user.id, username=user.username,
            event_type="REFRESH_FAILED", details="Refresh token expired",
            client_ip=client_ip, user_agent=user_agent
        )
        raise ValueError("Refresh token has expired. Please log in again.")

    # Rotate Token
    new_token_str, new_jti = generate_refresh_token()
    new_token_hash = hash_token(new_token_str)

    token_entry.revoked_at = now
    token_entry.replaced_by = new_jti

    new_refresh_model = models.RefreshTokenModel(
        id=str(uuid.uuid4()),
        jti=new_jti,
        user_id=user.id,
        token_hash=new_token_hash,
        created_at=now,
        expires_at=now + timedelta(days=settings.refresh_token_expire_days),
        revoked_at=None,
        replaced_by=None,
        user_agent=user_agent,
        client_ip=client_ip
    )
    db.add(new_refresh_model)
    db.commit()

    log_security_audit_event(
        db=db, user_id=user.id, username=user.username,
        event_type="REFRESH_SUCCESS", details=f"Rotated token JTI {token_entry.jti} -> {new_jti}",
        client_ip=client_ip, user_agent=user_agent
    )
    return new_token_str, user


def revoke_refresh_session(db: Session, refresh_token_str: str, user_id: Optional[str] = None):
    """Invalidates a refresh token session during logout."""
    token_hash_str = hash_token(refresh_token_str)
    token_entry = db.query(models.RefreshTokenModel).filter(models.RefreshTokenModel.token_hash == token_hash_str).first()
    now = datetime.now(timezone.utc)

    if token_entry and token_entry.revoked_at is None:
        token_entry.revoked_at = now
        db.commit()
        log_security_audit_event(
            db=db, user_id=token_entry.user_id, username=None,
            event_type="LOGOUT", details=f"Revoked token session JTI '{token_entry.jti}'"
        )


def revoke_all_user_sessions(db: Session, user_id: str, reason: str = "Sessions revoked by admin"):
    """Revokes all active refresh token sessions for a specific user ID."""
    now = datetime.now(timezone.utc)
    active_tokens = db.query(models.RefreshTokenModel).filter(
        models.RefreshTokenModel.user_id == user_id,
        models.RefreshTokenModel.revoked_at.is_(None)
    ).all()

    for t in active_tokens:
        t.revoked_at = now

    db.commit()
    user = get_user_by_id(db, user_id)
    log_security_audit_event(
        db=db, user_id=user_id, username=user.username if user else None,
        event_type="SESSIONS_REVOKED", details=reason
    )


def change_user_password(db: Session, user_id: str, current_password: str, new_password: str):
    """Changes a user's password and revokes all active refresh sessions."""
    user = get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found.")

    if not verify_password(current_password, user.password_hash):
        raise ValueError("Current password is incorrect.")

    user.password_hash = hash_password(new_password)
    user.updated_at = datetime.now(timezone.utc)
    db.commit()

    # Revoke existing refresh sessions upon password change
    revoke_all_user_sessions(db, user_id, reason="Password changed successfully")

    log_security_audit_event(
        db=db, user_id=user.id, username=user.username,
        event_type="PASSWORD_CHANGE", details="Password changed successfully"
    )


def update_user_status(db: Session, user_id: str, is_active: Optional[bool] = None, role: Optional[str] = None):
    """Updates user account status (active/disabled) and role."""
    user = get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found.")

    changes = []
    if is_active is not None and user.is_active != is_active:
        user.is_active = is_active
        changes.append(f"is_active={is_active}")
        if not is_active:
            revoke_all_user_sessions(db, user_id, reason="Account disabled by admin")

    if role is not None and user.role != role.upper():
        user.role = role.upper()
        changes.append(f"role={user.role}")

    if changes:
        user.updated_at = datetime.now(timezone.utc)
        db.commit()
        log_security_audit_event(
            db=db, user_id=user.id, username=user.username,
            event_type="USER_UPDATED", details=", ".join(changes)
        )
    return user


def seed_default_admin(db: Session) -> models.UserModel:
    """Seeds default admin user for development environment if no users exist."""
    admin_user = get_user_by_username(db, "admin")
    if not admin_user:
        admin_user = create_user(
            db=db,
            username="admin",
            email="admin@trustchain.local",
            password="Admin@TrustChain2026!",
            role="ADMIN",
            is_active=True,
            created_by_admin=True
        )
        logger.info("Default admin user created: admin / Admin@TrustChain2026!")
    return admin_user

import pytest
import time
from datetime import datetime, timedelta, timezone
import jwt
from fastapi.testclient import TestClient

from akta.server import app
from akta.config import settings
from akta.vdr.database import get_db
from akta.vdr import models
from akta.auth import security, crud, schemas

client = TestClient(app)


def get_db_session():
    db_gen = get_db()
    db = next(db_gen)
    return db


# ==========================================
# 1. Password Hashing & Security Tests
# ==========================================

def test_hash_password_differs_from_plain():
    plain = "SecurePassword123!"
    hashed = security.hash_password(plain)
    assert hashed != plain
    assert len(hashed) > 20


def test_verify_correct_password():
    plain = "SecurePassword123!"
    hashed = security.hash_password(plain)
    assert security.verify_password(plain, hashed) is True


def test_verify_incorrect_password():
    plain = "SecurePassword123!"
    hashed = security.hash_password(plain)
    assert security.verify_password("WrongPassword123!", hashed) is False


# ==========================================
# 2. User Authentication & Login Tests
# ==========================================

def test_login_success_admin():
    response = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "Admin@TrustChain2026!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["username"] == "admin"
    assert data["user"]["role"] == "ADMIN"


def test_login_success_case_insensitive_username():
    response = client.post("/api/v1/auth/login", json={
        "username": "AdMiN",
        "password": "Admin@TrustChain2026!"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["username"] == "admin"


def test_login_invalid_password():
    response = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "WrongPassword123!"
    })
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_login_nonexistent_user():
    response = client.post("/api/v1/auth/login", json={
        "username": "nonexistent_user_99",
        "password": "Password123!"
    })
    assert response.status_code == 401


def test_login_disabled_account():
    db = get_db_session()
    try:
        username = "disabled_test_user"
        try:
            crud.create_user(db, username=username, password="Password123!", role="VIEWER", is_active=False)
        except ValueError:
            pass

        response = client.post("/api/v1/auth/login", json={
            "username": username,
            "password": "Password123!"
        })
        assert response.status_code == 401
        assert "disabled" in response.json()["detail"].lower()
    finally:
        db.close()


# ==========================================
# 3. Account Lockout & Brute-Force Protection
# ==========================================

def test_brute_force_lockout():
    db = get_db_session()
    try:
        username = "lockout_test_user"
        try:
            crud.create_user(db, username=username, password="CorrectPassword123!", role="OPERATOR")
        except ValueError:
            pass

        # 5 failed login attempts
        for i in range(5):
            res = client.post("/api/v1/auth/login", json={"username": username, "password": "WrongPassword!"})
            assert res.status_code == 401

        # 6th attempt must return account locked message
        locked_res = client.post("/api/v1/auth/login", json={"username": username, "password": "CorrectPassword123!"})
        assert locked_res.status_code == 401
        assert "locked" in locked_res.json()["detail"].lower()
    finally:
        db.close()


# ==========================================
# 4. JWT Access Tokens
# ==========================================

def test_create_and_decode_access_token():
    token = security.create_access_token(user_id="usr_123", username="testuser", role="OPERATOR")
    payload = security.decode_access_token(token)
    assert payload["sub"] == "usr_123"
    assert payload["username"] == "testuser"
    assert payload["role"] == "OPERATOR"


def test_decode_expired_jwt():
    past = datetime.now(timezone.utc) - timedelta(hours=2)
    payload = {
        "sub": "usr_123",
        "username": "testuser",
        "role": "VIEWER",
        "exp": past,
        "iat": past - timedelta(minutes=30),
        "type": "access"
    }
    expired_token = jwt.encode(payload, settings.auth_secret, algorithm="HS256")
    
    with pytest.raises(ValueError, match="expired|invalid"):
        security.decode_access_token(expired_token)


def test_decode_tampered_jwt():
    token = security.create_access_token(user_id="usr_123", username="testuser", role="OPERATOR")
    tampered = token[:-5] + "XXXXX"
    with pytest.raises(ValueError):
        security.decode_access_token(tampered)


# ==========================================
# 5. Refresh Token Rotation & Reuse Detection
# ==========================================

def test_refresh_token_rotation():
    login_res = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@TrustChain2026!"})
    assert login_res.status_code == 200
    rt1 = login_res.json()["refresh_token"]

    refresh_res = client.post("/api/v1/auth/refresh", json={"refresh_token": rt1})
    assert refresh_res.status_code == 200
    refreshed_data = refresh_res.json()
    assert "access_token" in refreshed_data
    rt2 = refreshed_data["refresh_token"]
    assert rt2 != rt1


def test_refresh_token_reuse_detection():
    login_res = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@TrustChain2026!"})
    rt1 = login_res.json()["refresh_token"]

    # First refresh succeeds and rotates token
    res1 = client.post("/api/v1/auth/refresh", json={"refresh_token": rt1})
    assert res1.status_code == 200

    # Second refresh with OLD token (rt1) must trigger reuse detection and revoke session
    res2 = client.post("/api/v1/auth/refresh", json={"refresh_token": rt1})
    assert res2.status_code == 401
    assert "reuse" in res2.json()["detail"].lower()


def test_invalid_refresh_token():
    res = client.post("/api/v1/auth/refresh", json={"refresh_token": "invalid_token_string_12345"})
    assert res.status_code == 401


# ==========================================
# 6. Logout & Session Revocation
# ==========================================

def test_logout_invalidates_session():
    login_res = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@TrustChain2026!"})
    rt = login_res.json()["refresh_token"]
    at = login_res.json()["access_token"]

    logout_res = client.post("/api/v1/auth/logout", json={"refresh_token": rt}, headers={"Authorization": f"Bearer {at}"})
    assert logout_res.status_code == 200

    # Subsequent refresh with revoked token fails
    refresh_res = client.post("/api/v1/auth/refresh", json={"refresh_token": rt})
    assert refresh_res.status_code == 401


# ==========================================
# 7. Role-Based Access Control (RBAC) Tests
# ==========================================

def test_rbac_admin_access_admin_route():
    login_res = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@TrustChain2026!"})
    at = login_res.json()["access_token"]

    users_res = client.get("/api/v1/auth/users", headers={"Authorization": f"Bearer {at}"})
    assert users_res.status_code == 200
    assert isinstance(users_res.json(), list)


def test_rbac_operator_denied_admin_route():
    db = get_db_session()
    try:
        username = "operator_rbac_user"
        try:
            crud.create_user(db, username=username, password="Password123!", role="OPERATOR")
        except ValueError:
            pass
    finally:
        db.close()

    login_res = client.post("/api/v1/auth/login", json={"username": "operator_rbac_user", "password": "Password123!"})
    at = login_res.json()["access_token"]

    users_res = client.get("/api/v1/auth/users", headers={"Authorization": f"Bearer {at}"})
    assert users_res.status_code == 403


def test_rbac_viewer_denied_admin_route():
    db = get_db_session()
    try:
        username = "viewer_rbac_user"
        try:
            crud.create_user(db, username=username, password="Password123!", role="VIEWER")
        except ValueError:
            pass
    finally:
        db.close()

    login_res = client.post("/api/v1/auth/login", json={"username": "viewer_rbac_user", "password": "Password123!"})
    at = login_res.json()["access_token"]

    users_res = client.get("/api/v1/auth/users", headers={"Authorization": f"Bearer {at}"})
    assert users_res.status_code == 403


def test_rbac_admin_revoke_agent_did():
    # Register an agent
    reg = client.post("/api/v1/registry/agents", json={"agent_name": "Revoke Test Agent", "capabilities": "general"}).json()
    did = reg["did"]

    # Login as admin
    admin_at = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@TrustChain2026!"}).json()["access_token"]

    # Admin calls POST /trust/revoke/{did}
    revoke_res = client.post(
        f"/api/v1/trust/revoke/{did}",
        json={"reason": "Security compromise test"},
        headers={"Authorization": f"Bearer {admin_at}"}
    )
    assert revoke_res.status_code == 200
    assert revoke_res.json()["trust_state"] == "REVOKED"


def test_rbac_non_admin_revoke_agent_did():
    reg = client.post("/api/v1/registry/agents", json={"agent_name": "Revoke Guard Agent", "capabilities": "general"}).json()
    did = reg["did"]

    # Create operator user
    db = get_db_session()
    try:
        try:
            crud.create_user(db, username="operator_guard", password="Password123!", role="OPERATOR")
        except ValueError:
            pass
    finally:
        db.close()

    op_at = client.post("/api/v1/auth/login", json={"username": "operator_guard", "password": "Password123!"}).json()["access_token"]

    # Operator attempting to revoke agent DID should be rejected (403)
    revoke_res = client.post(
        f"/api/v1/trust/revoke/{did}",
        json={"reason": "Unauthorized attempt"},
        headers={"Authorization": f"Bearer {op_at}"}
    )
    assert revoke_res.status_code == 403


# ==========================================
# 8. User Governance & Admin Management Tests
# ==========================================

def test_admin_create_new_user():
    import uuid
    admin_at = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@TrustChain2026!"}).json()["access_token"]
    uname = f"gov_user_{uuid.uuid4().hex[:6]}"

    new_user_res = client.post("/api/v1/auth/users", json={
        "username": uname,
        "email": f"{uname}@trustchain.local",
        "password": "Password123!",
        "role": "OPERATOR"
    }, headers={"Authorization": f"Bearer {admin_at}"})

    assert new_user_res.status_code == 200
    data = new_user_res.json()
    assert data["username"] == uname
    assert data["role"] == "OPERATOR"


def test_admin_create_duplicate_user():
    admin_at = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@TrustChain2026!"}).json()["access_token"]

    dup_res = client.post("/api/v1/auth/users", json={
        "username": "admin",
        "password": "Password123!",
        "role": "OPERATOR"
    }, headers={"Authorization": f"Bearer {admin_at}"})

    assert dup_res.status_code == 400


def test_admin_update_user_status():
    import uuid
    admin_at = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@TrustChain2026!"}).json()["access_token"]
    uname = f"status_user_{uuid.uuid4().hex[:6]}"

    # Create target user
    u_res = client.post("/api/v1/auth/users", json={
        "username": uname,
        "password": "Password123!",
        "role": "VIEWER"
    }, headers={"Authorization": f"Bearer {admin_at}"}).json()

    user_id = u_res["id"]

    # Disable user
    patch_res = client.patch(f"/api/v1/auth/users/{user_id}/status", json={
        "is_active": False,
        "role": "VIEWER"
    }, headers={"Authorization": f"Bearer {admin_at}"})

    assert patch_res.status_code == 200
    assert patch_res.json()["is_active"] is False


def test_admin_revoke_user_sessions():
    admin_at = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@TrustChain2026!"}).json()["access_token"]

    # Create user and log in as that user
    db = get_db_session()
    try:
        try:
            crud.create_user(db, username="session_target", password="Password123!", role="OPERATOR")
        except ValueError:
            pass
    finally:
        db.close()

    target_res = client.post("/api/v1/auth/login", json={"username": "session_target", "password": "Password123!"}).json()
    target_rt = target_res["refresh_token"]

    # Admin revokes session_target's sessions
    users_list = client.get("/api/v1/auth/users", headers={"Authorization": f"Bearer {admin_at}"}).json()
    target_obj = next(u for u in users_list if u["username"] == "session_target")

    revoke_res = client.post(f"/api/v1/auth/users/{target_obj['id']}/revoke-sessions", headers={"Authorization": f"Bearer {admin_at}"})
    assert revoke_res.status_code == 200

    # Verify session_target's refresh token no longer works
    ref_res = client.post("/api/v1/auth/refresh", json={"refresh_token": target_rt})
    assert ref_res.status_code == 401


# ==========================================
# 9. Password Change Flow Tests
# ==========================================

def test_user_change_password_success():
    import uuid
    uname = f"change_pass_{uuid.uuid4().hex[:6]}"
    db = get_db_session()
    try:
        crud.create_user(db, username=uname, password="OldPassword123!", role="OPERATOR")
    finally:
        db.close()

    login_res = client.post("/api/v1/auth/login", json={"username": uname, "password": "OldPassword123!"}).json()
    at = login_res["access_token"]

    change_res = client.post("/api/v1/auth/change-password", json={
        "current_password": "OldPassword123!",
        "new_password": "NewPassword123!"
    }, headers={"Authorization": f"Bearer {at}"})
    assert change_res.status_code == 200

    # Verify old password fails
    fail_res = client.post("/api/v1/auth/login", json={"username": uname, "password": "OldPassword123!"})
    assert fail_res.status_code == 401

    # Verify new password succeeds
    succ_res = client.post("/api/v1/auth/login", json={"username": uname, "password": "NewPassword123!"})
    assert succ_res.status_code == 200


def test_user_change_password_wrong_current():
    db = get_db_session()
    try:
        try:
            crud.create_user(db, username="wrong_curr_user", password="OriginalPass123!", role="OPERATOR")
        except ValueError:
            pass
    finally:
        db.close()

    login_res = client.post("/api/v1/auth/login", json={"username": "wrong_curr_user", "password": "OriginalPass123!"}).json()
    at = login_res["access_token"]

    change_res = client.post("/api/v1/auth/change-password", json={
        "current_password": "IncorrectPass123!",
        "new_password": "BrandNewPass123!"
    }, headers={"Authorization": f"Bearer {at}"})
    assert change_res.status_code == 400


# ==========================================
# 10. Security Audit Logging Tests
# ==========================================

def test_security_audit_events_recorded():
    admin_at = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@TrustChain2026!"}).json()["access_token"]

    audit_res = client.get("/api/v1/auth/audit?limit=50", headers={"Authorization": f"Bearer {admin_at}"})
    assert audit_res.status_code == 200
    events = audit_res.json()
    assert len(events) > 0
    
    event_types = [e["event_type"] for e in events]
    assert "LOGIN_SUCCESS" in event_types

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from akta.server import app

client = TestClient(app)

def test_system_health_healthy():
    """Verify that the authoritative health endpoint returns 200 OK and all subsystem probes pass."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "ok"
    assert "components" in data
    assert "fastapi" in data["components"]
    assert "database" in data["components"]
    assert "trust_engine" in data["components"]
    
    # Check FastAPI component
    fastapi_comp = data["components"]["fastapi"]
    assert fastapi_comp["status"] == "ok"
    assert fastapi_comp["port"] == 8050
    
    # Check SQLite VDR component
    db_comp = data["components"]["database"]
    assert db_comp["status"] == "ok"
    assert db_comp["engine"] == "sqlite"
    assert db_comp["mode"] == "WAL"
    assert db_comp["latency_ms"] >= 0
    assert db_comp["error"] is None
    
    # Check Trust Math Core component
    trust_comp = data["components"]["trust_engine"]
    assert trust_comp["status"] == "ok"
    assert trust_comp["mode"] == "in-process"
    assert trust_comp["weights"]["w1_success"] == 0.6
    assert trust_comp["weights"]["decay_lambda"] == 0.7
    assert trust_comp["error"] is None


def test_system_health_database_failure_simulation():
    """Verify that when database connection fails, /health reports degraded with error details without crashing."""
    with patch("akta.server.SessionLocal", side_effect=Exception("Simulated SQLite disk/lock failure")):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "degraded"
        assert data["components"]["database"]["status"] == "error"
        assert "Simulated SQLite disk/lock failure" in data["components"]["database"]["error"]
        # Other subsystems should still report their actual status
        assert data["components"]["fastapi"]["status"] == "ok"
        assert data["components"]["trust_engine"]["status"] == "ok"


def test_system_health_trust_engine_failure_simulation():
    """Verify that when trust engine math verification fails, /health reports degraded without crashing."""
    with patch("akta.trust_engine.TrustEngine.calculate_behavioral_score", side_effect=ValueError("Simulated math calculation anomaly")):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "degraded"
        assert data["components"]["trust_engine"]["status"] == "error"
        assert "Simulated math calculation anomaly" in data["components"]["trust_engine"]["error"]
        # Database and FastAPI should remain healthy
        assert data["components"]["fastapi"]["status"] == "ok"
        assert data["components"]["database"]["status"] == "ok"


def test_system_health_simultaneous_failure():
    """Verify that if both subsystems fail, /health reports degraded and records both error details."""
    with patch("akta.server.SessionLocal", side_effect=Exception("Database down")), \
         patch("akta.trust_engine.TrustEngine.calculate_behavioral_score", side_effect=RuntimeError("Engine failure")):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "degraded"
        assert data["components"]["database"]["status"] == "error"
        assert data["components"]["trust_engine"]["status"] == "error"
        assert data["components"]["fastapi"]["status"] == "ok"

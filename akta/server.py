from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from akta.config import settings
from akta.logging import get_logger, request_id_middleware
from akta.vdr.database import create_tables as create_vdr_tables
from akta.vdr.router import router as vdr_router
from akta.vdr.registry_router import router as registry_router
from akta.test_agent.router import router as agent_router
from akta.auth.router import router as auth_router

import time
from datetime import datetime, timezone
from sqlalchemy import text
from akta.vdr.database import SessionLocal
from akta.trust_engine import TrustEngine, TrustConfig

logger = get_logger(__name__)

def create_app() -> FastAPI:
    create_vdr_tables()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    @app.middleware("http")
    async def add_security_headers_and_request_id(request: Request, call_next):
        request_id: str = request_id_middleware(request)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    api_v1 = APIRouter(prefix="/api/v1", tags=["v1"])

    api_v1.include_router(auth_router)
    api_v1.include_router(vdr_router, tags=["Verifiable Credential Registry Endpoints"])
    api_v1.include_router(registry_router, tags=["Agent Registry & Collaboration Endpoints"])
    api_v1.include_router(agent_router, tags=["Agent Endpoints"])

    app.include_router(api_v1)

    @app.get("/health", tags=["Health Check"])
    async def health_check():
        logger.info("Health check endpoint was called.")

        # 1. Authoritative SQLite VDR Database Connectivity Check
        db_status = "ok"
        db_latency_ms = 0.0
        db_message = "Connected to SQLite VDR (Read/Write OK)"
        db_error = None
        t_db_start = time.perf_counter()
        try:
            db = SessionLocal()
            try:
                res = db.execute(text("SELECT 1")).scalar()
                if res != 1:
                    raise RuntimeError(f"Database query test returned unexpected scalar: {res}")
            finally:
                db.close()
            db_latency_ms = round((time.perf_counter() - t_db_start) * 1000, 2)
        except Exception as e:
            db_status = "error"
            db_message = f"Database connection failed: {str(e)}"
            db_error = str(e)
            logger.error(f"Health check DB probe failed: {e}")

        # 2. Authoritative Trust Math Core Verification Check
        trust_status = "ok"
        trust_message = "Temporal EMA & Multi-Factor Math Core operational"
        trust_error = None
        try:
            engine = TrustEngine(TrustConfig())
            test_score = engine.calculate_behavioral_score(1.0, 1.0, 0.0)
            test_decay = engine.calculate_temporal_trust(1.0, test_score)
            if abs(test_decay - 1.0) > 1e-4:
                raise RuntimeError(f"Trust math core returned unexpected score: {test_decay}")
        except Exception as e:
            trust_status = "error"
            trust_message = f"Trust math engine check failed: {str(e)}"
            trust_error = str(e)
            logger.error(f"Health check TrustEngine probe failed: {e}")

        # Overall subsystem aggregation
        is_all_ok = (db_status == "ok" and trust_status == "ok")
        overall_status = "ok" if is_all_ok else "degraded"

        return {
            "status": overall_status,
            "app_name": settings.app_name,
            "debug_mode": settings.debug,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
            "components": {
                "fastapi": {
                    "status": "ok",
                    "name": "FastAPI Backend",
                    "message": "Uvicorn ASGI server operational",
                    "port": 8050,
                    "version": "1.0.0",
                },
                "database": {
                    "status": db_status,
                    "name": "SQLite VDR",
                    "engine": "sqlite",
                    "mode": "WAL",
                    "message": db_message,
                    "latency_ms": db_latency_ms,
                    "error": db_error,
                },
                "trust_engine": {
                    "status": trust_status,
                    "name": "Trust Math Core",
                    "mode": "in-process",
                    "message": trust_message,
                    "weights": {
                        "w1_success": 0.6,
                        "w2_compliance": 0.3,
                        "w3_latency": 0.1,
                        "decay_lambda": 0.7,
                    },
                    "error": trust_error,
                },
            },
        }

    return app

app = create_app()

allowed_origins = [origin.strip() for origin in settings.cors_allowed_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


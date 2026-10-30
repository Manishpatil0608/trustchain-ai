from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from akta.logging import get_logger

logger = get_logger(__name__)

SQLALCHEMY_DATABASE_URL = "sqlite:///./vdr.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False, "timeout": 30}
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get a DB session for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Creates all database tables defined by models inheriting from Base."""
    Base.metadata.create_all(bind=engine)
    logger.info(f"Database tables created (if they didn't exist) at {SQLALCHEMY_DATABASE_URL}")

    # Auto-seed default admin account if enabled in settings
    try:
        from akta.config import settings
        if getattr(settings, "dev_auto_seed_admin", True):
            db = SessionLocal()
            try:
                from akta.auth.crud import seed_default_admin
                seed_default_admin(db)
            except Exception as e:
                logger.error(f"Could not auto-seed admin account: {e}")
            finally:
                db.close()
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")


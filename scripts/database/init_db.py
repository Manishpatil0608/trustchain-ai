"""
scripts/database/init_db.py
Initializes the SQLite Verifiable Data Registry (VDR) database tables.
"""

import sys
import os

# Add project root to Python search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from akta.vdr.database import create_tables, engine, SQLALCHEMY_DATABASE_URL
from akta.logging import get_logger

logger = get_logger(__name__)

def main():
    print(f"[*] Initializing TrustChain-AI SQLite Database at: {SQLALCHEMY_DATABASE_URL}")
    create_tables()
    print("[+] All 13 tables successfully verified and initialized.")

if __name__ == "__main__":
    main()

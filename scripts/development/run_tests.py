"""
scripts/development/run_tests.py
Executes the comprehensive automated verification suite for TrustChain-AI:
1. Backend Pytest test suite (80 test scenarios)
2. Frontend Oxlint and Vite production build
"""

import sys
import os
import subprocess

def run_backend_tests(base_dir):
    print("============================================================")
    print("1. Running Backend Pytest Test Suite")
    print("============================================================")
    cmd = [sys.executable, "-m", "pytest", os.path.join(base_dir, "tests"), "-v"]
    res = subprocess.run(cmd, cwd=base_dir)
    return res.returncode == 0

def run_frontend_build(base_dir):
    print("\n============================================================")
    print("2. Running Frontend Production Build (Vite)")
    print("============================================================")
    frontend_dir = os.path.join(base_dir, "frontend")
    cmd = "npm run build"
    res = subprocess.run(cmd, shell=True, cwd=frontend_dir)
    return res.returncode == 0

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    b_ok = run_backend_tests(base_dir)
    f_ok = run_frontend_build(base_dir)

    print("\n============================================================")
    print("Verification Summary:")
    print(f"  Backend Tests (80 Items): {'PASS' if b_ok else 'FAIL'}")
    print(f"  Frontend Vite Build:      {'PASS' if f_ok else 'FAIL'}")
    print("============================================================")

    if not (b_ok and f_ok):
        sys.exit(1)

if __name__ == "__main__":
    main()

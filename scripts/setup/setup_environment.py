"""
scripts/setup/setup_environment.py
Validates the developer environment, prerequisites, and system dependencies
for TrustChain-AI.
"""

import sys
import os
import shutil
import subprocess

def check_python():
    print("[*] Checking Python version...")
    v = sys.version_info
    print(f"    Detected Python: {v.major}.{v.minor}.{v.micro}")
    if v.major != 3 or v.minor < 11:
        print("    [!] ERROR: TrustChain-AI requires Python 3.11 or newer.")
        return False
    print("    [+] Python version satisfies >= 3.11 requirement.")
    return True

def check_node():
    print("[*] Checking Node.js and npm...")
    node_path = shutil.which("node")
    npm_path = shutil.which("npm")

    if not node_path:
        print("    [!] WARNING: Node.js was not detected in PATH.")
        return False
    else:
        try:
            node_ver = subprocess.check_output(["node", "--version"]).decode().strip()
            print(f"    [+] Node.js detected: {node_ver}")
        except Exception as e:
            print(f"    [!] Could not read node version: {e}")

    if not npm_path:
        print("    [!] WARNING: npm was not detected in PATH.")
        return False
    else:
        try:
            npm_ver = subprocess.check_output(["npm", "--version"]).decode().strip()
            print(f"    [+] npm detected: {npm_ver}")
        except Exception as e:
            print(f"    [!] Could not read npm version: {e}")
    return True

def check_env_file():
    print("[*] Checking backend environment configuration (.env)...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_file = os.path.join(base_dir, ".env")
    example_file = os.path.join(base_dir, ".env.example")

    if os.path.exists(env_file):
        print("    [+] Active .env configuration file exists.")
    else:
        print("    [-] .env not found. Auto-generating from .env.example...")
        if os.path.exists(example_file):
            shutil.copy2(example_file, env_file)
            print("    [+] Created .env from .env.example successfully.")
        else:
            print("    [!] ERROR: Neither .env nor .env.example was found.")
            return False
    return True

def main():
    print("============================================================")
    print("TrustChain-AI Environment Health & Sanity Check")
    print("============================================================\n")

    p_ok = check_python()
    n_ok = check_node()
    e_ok = check_env_file()

    print("\n------------------------------------------------------------")
    if p_ok and n_ok and e_ok:
        print("[+] All core prerequisites and configuration checks passed!")
        print("    To initialize the database: python scripts/database/init_db.py")
        print("    To seed demo agents:      python scripts/database/seed_demo_data.py")
        print("    To start full platform:   START_TRUSTCHAIN.bat (Windows)")
    else:
        print("[!] Some components require attention. Review the output above.")
    print("============================================================")

if __name__ == "__main__":
    main()

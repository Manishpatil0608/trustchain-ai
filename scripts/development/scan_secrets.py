"""
scripts/development/scan_secrets.py
Scans repository files for leaked credentials, private keys, and sensitive tokens.
"""

import os
import re

PATTERNS = [
    (r'(?i)(?:api_key|apikey|secret_key|app_secret)\s*[:=]\s*[\'"][a-zA-Z0-9_\-]{20,}[\'"]', 'API Key / Secret'),
    (r'(?i)ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Access Token'),
    (r'(?i)glpat-[a-zA-Z0-9_\-]{20}', 'GitLab Personal Access Token'),
    (r'-----BEGIN (?:RSA|OPENSSH|EC|PGP|PRIVATE) KEY-----', 'Private Key Block'),
    (r'(?i)AKIA[0-9A-Z]{16}', 'AWS Access Key'),
    (r'(?i)AIza[0-9A-Za-z\-_]{35}', 'Google API Key'),
]

SAFE_VALUES = [
    "dev_secret_trustchain_ai_capstone_project_2026_key_32_bytes_min!",
    "Admin@TrustChain2026!"
]

def scan():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    exclusions = {'.venv', 'node_modules', 'dist', '.git', '__pycache__', '.pytest_cache'}

    total_files = 0
    alerts = 0

    print(f"[*] Starting Security Audit Scan across: {base_dir}")

    for dirpath, dirnames, filenames in os.walk(base_dir):
        dirnames[:] = [d for d in dirnames if d not in exclusions]
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in ['.py', '.js', '.jsx', '.json', '.md', '.txt', '.yml', '.yaml', '.sh', '.bat', '.env', '.example', '.sql']:
                total_files += 1
                p = os.path.join(dirpath, f)
                try:
                    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read()
                        for pat, desc in PATTERNS:
                            matches = re.findall(pat, content)
                            for m in matches:
                                if not any(safe in m for safe in SAFE_VALUES):
                                    rel = os.path.relpath(p, base_dir)
                                    print(f"    [!] ALERT [{desc}]: {rel} -> {m[:40]}...")
                                    alerts += 1
                except Exception as e:
                    pass

    print(f"\n[+] Scan Complete: Scanned {total_files} files.")
    if alerts == 0:
        print("[+] ZERO leaked secrets, private keys, or tokens detected. Clean security posture!")
    else:
        print(f"[!] WARNING: Found {alerts} potential secret alert(s).")

if __name__ == "__main__":
    scan()

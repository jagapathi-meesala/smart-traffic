"""Security Audit tool scanning project directory for secret leaks and key exposure."""

import os
import re
from typing import Dict, Any, List, Optional


class SecurityAudit:
    """Scans project files for exposed secrets, API keys, and un-ignored credentials."""

    SUSPICIOUS_PATTERNS = [
        re.compile(r"sk-[a-zA-Z0-9]{20,}", re.IGNORECASE),
        re.compile(r"api_key\s*=\s*['\"][a-zA-Z0-9_\-]{16,}['\"]", re.IGNORECASE),
        re.compile(r"password\s*=\s*['\"][^'\"]+['\"]", re.IGNORECASE),
        re.compile(r"bearer\s+[a-zA-Z0-9_\-\.]{20,}", re.IGNORECASE),
    ]

    def __init__(self, root_dir: Optional[str] = None):
        if root_dir is None:
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.root_dir = root_dir

    def run_audit(self) -> Dict[str, Any]:
        """Perform automated security audit."""
        findings = []

        # 1. Check .gitignore presence and .env rule
        gitignore_path = os.path.join(self.root_dir, ".gitignore")
        env_ignored = False
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r", encoding="utf-8") as f:
                content = f.read()
                if ".env" in content:
                    env_ignored = True

        if not env_ignored:
            findings.append("CRITICAL: .env is not explicitly listed in .gitignore file.")

        # 2. Check .env.example presence
        env_example_path = os.path.join(self.root_dir, ".env.example")
        has_env_example = os.path.exists(env_example_path)
        if not has_env_example:
            findings.append("WARNING: .env.example file is missing.")

        # 3. Code scan for credentials
        scanned_files = 0
        for root, dirs, files in os.walk(self.root_dir):
            # Skip git and cache dirs
            dirs[:] = [d for d in dirs if d not in [".git", "__pycache__", ".pytest_cache", "venv", ".venv"]]
            for file in files:
                if file.endswith((".py", ".yaml", ".yml", ".json", ".md")):
                    filepath = os.path.join(root, file)
                    scanned_files += 1
                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            lines = f.readlines()
                            for idx, line in enumerate(lines, 1):
                                # Ignore template examples or comments in .env.example / config
                                if "OPENAI_API_KEY=" in line and ("example" in filepath.lower() or "settings.py" in filepath.lower()):
                                    continue
                                for pattern in self.SUSPICIOUS_PATTERNS:
                                    if pattern.search(line):
                                        findings.append(f"Potential secret match in {os.path.relpath(filepath, self.root_dir)}:L{idx}")
                    except Exception:
                        pass

        is_secure = len(findings) == 0

        return {
            "status": "PASSED" if is_secure else "FAILED",
            "is_secure": is_secure,
            "scanned_files_count": scanned_files,
            "env_ignored_in_gitignore": env_ignored,
            "env_example_exists": has_env_example,
            "findings_count": len(findings),
            "findings": findings,
        }

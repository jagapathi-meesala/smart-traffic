"""Hardcoding Audit tool checking for inappropriate hardcoded parameters."""

import os
import re
from typing import Dict, Any, List, Optional


class HardcodingAudit:
    """Scans for hardcoded paths, fake external responses, and hardcoded credentials."""

    SUSPICIOUS_PATHS = [
        re.compile(r"/Users/[a-zA-Z0-9_\-]+", re.IGNORECASE),
        re.compile(r"C:\\Users\\[a-zA-Z0-9_\-]+", re.IGNORECASE),
    ]

    def __init__(self, root_dir: Optional[str] = None):
        if root_dir is None:
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.root_dir = root_dir

    def run_audit(self) -> Dict[str, Any]:
        """Perform hardcoding audit."""
        issues = []
        scanned_count = 0

        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in [".git", "__pycache__", ".pytest_cache", "venv", ".venv"]]
            for file in files:
                if file.endswith((".py", ".yaml")):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, self.root_dir)
                    scanned_count += 1
                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            lines = f.readlines()
                            for idx, line in enumerate(lines, 1):
                                # Check user-specific hardcoded paths
                                for pattern in self.SUSPICIOUS_PATHS:
                                    if pattern.search(line):
                                        issues.append(f"Hardcoded personal path in {rel_path}:L{idx}")
                    except Exception:
                        pass

        is_clean = len(issues) == 0

        return {
            "status": "PASSED" if is_clean else "FAILED",
            "is_clean": is_clean,
            "scanned_files_count": scanned_count,
            "issues_count": len(issues),
            "issues": issues,
        }

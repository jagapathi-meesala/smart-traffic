"""HiDevs Readiness Verifier for Agent Passport Challenge submission compliance."""

import os
import yaml
from typing import Dict, Any, List, Optional
from passport.passport_manager import PassportManager
from verification.security_audit import SecurityAudit


class HiDevsReadinessVerifier:
    """Verifies all Agent Passport & HiDevs submission criteria locally."""

    REQUIRED_EXPLAINABILITY_HEADINGS = [
        "## Purpose",
        "## Inputs and Data Sources",
        "## Decision and Reasoning",
        "## Tools and Capabilities",
        "## Limitations and Constraints",
        "## Portability",
        "## Verification",
        "## Failure Handling",
        "## Expected Output",
    ]

    def __init__(self, root_dir: Optional[str] = None):
        if root_dir is None:
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.root_dir = root_dir

    def verify_readiness(self) -> Dict[str, Any]:
        """Verify project submission readiness."""
        checks: Dict[str, bool] = {}
        issues: List[str] = []

        # 1. agent.yaml check
        agent_yaml_path = os.path.join(self.root_dir, "agent.yaml")
        if not os.path.exists(agent_yaml_path):
            checks["agent_yaml_exists"] = False
            issues.append("agent.yaml file does not exist")
        else:
            checks["agent_yaml_exists"] = True
            pm = PassportManager(agent_yaml_path)
            res = pm.validate_passport()
            checks["passport_valid"] = res.is_valid
            if not res.is_valid:
                issues.extend(res.errors)

        # 2. Documentation files check
        soul_path = os.path.join(self.root_dir, "SOUL.md")
        duties_path = os.path.join(self.root_dir, "DUTIES.md")
        explainability_path = os.path.join(self.root_dir, "EXPLAINABILITY.md")

        checks["soul_md_exists"] = os.path.exists(soul_path)
        if not checks["soul_md_exists"]:
            issues.append("SOUL.md file missing")

        checks["duties_md_exists"] = os.path.exists(duties_path)
        if not checks["duties_md_exists"]:
            issues.append("DUTIES.md file missing")

        checks["explainability_md_exists"] = os.path.exists(explainability_path)
        if not checks["explainability_md_exists"]:
            issues.append("EXPLAINABILITY.md file missing")
        else:
            # Check required headings in EXPLAINABILITY.md
            with open(explainability_path, "r", encoding="utf-8") as f:
                exp_text = f.read()

            missing_headings = [h for h in self.REQUIRED_EXPLAINABILITY_HEADINGS if h not in exp_text]
            checks["explainability_headings_valid"] = len(missing_headings) == 0
            if missing_headings:
                issues.append(f"EXPLAINABILITY.md missing required section headings: {missing_headings}")

        # 3. Security audit check
        sec_audit = SecurityAudit(self.root_dir)
        sec_res = sec_audit.run_audit()
        checks["security_clean"] = sec_res["is_secure"]
        if not sec_res["is_secure"]:
            issues.extend(sec_res["findings"])

        all_passed = all(checks.values()) and len(issues) == 0

        readiness_status = "READY" if all_passed else "NOT_READY"

        return {
            "readiness_status": readiness_status,
            "all_checks_passed": all_passed,
            "checks": checks,
            "issues_count": len(issues),
            "issues": issues,
            "disclaimer": "Local audit result only; does not replace official HiDevs competition grading.",
        }

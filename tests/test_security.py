"""Tests for SecurityAudit and HardcodingAudit."""

import pytest
from verification.security_audit import SecurityAudit
from verification.hardcoding_audit import HardcodingAudit


def test_security_audit():
    audit = SecurityAudit()
    res = audit.run_audit()
    assert res["status"] == "PASSED"
    assert res["is_secure"] is True
    assert res["env_ignored_in_gitignore"] is True
    assert res["env_example_exists"] is True
    assert res["findings_count"] == 0


def test_hardcoding_audit():
    audit = HardcodingAudit()
    res = audit.run_audit()
    assert res["status"] == "PASSED"
    assert res["is_clean"] is True
    assert res["issues_count"] == 0

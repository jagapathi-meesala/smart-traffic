"""Tests for HiDevsReadinessVerifier."""

import pytest
from verification.hidevs_readiness import HiDevsReadinessVerifier


def test_hidevs_readiness_verifier():
    verifier = HiDevsReadinessVerifier()
    res = verifier.verify_readiness()
    assert res["readiness_status"] == "READY"
    assert res["all_checks_passed"] is True
    assert res["issues_count"] == 0

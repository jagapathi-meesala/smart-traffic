"""Tests for PortabilityVerifier."""

import pytest
from verification.portability_verifier import PortabilityVerifier


def test_portability_verifier():
    verifier = PortabilityVerifier()
    res = verifier.verify_portability()
    assert res["status"] == "PASSED"
    assert res["is_portable"] is True
    assert res["framework_independent"] is True

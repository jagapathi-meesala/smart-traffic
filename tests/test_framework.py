"""Tests for FrameworkVerifier."""

import pytest
from verification.framework_verifier import FrameworkVerifier


def test_framework_verifier():
    verifier = FrameworkVerifier()
    res = verifier.verify_framework()
    assert res["status"] == "PASSED"
    assert res["structural_adapter_present"] is True

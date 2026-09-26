"""Tests for PassportManager and Passport schemas."""

import pytest
from passport.passport_manager import PassportManager


def test_passport_manager_load_and_validate():
    pm = PassportManager()
    manifest = pm.load_passport()

    assert manifest.spec_version == "0.1.0"
    assert manifest.name == "smart-traffic-management-agent"
    assert manifest.class_name == "SmartTrafficManagementAgent"
    assert len(manifest.capabilities) == 7
    assert len(manifest.tools) == 7

    res = pm.validate_passport()
    assert res.is_valid is True
    assert len(res.errors) == 0
    assert len(res.verified_capabilities) == 7
    assert len(res.verified_tools) == 7


def test_passport_manager_missing_file():
    pm = PassportManager("non_existent_passport.yaml")
    with pytest.raises(FileNotFoundError):
        pm.load_passport()

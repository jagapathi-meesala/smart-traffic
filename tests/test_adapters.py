"""Tests for PortableAdapter, FrameworkAdapter, and OpenAIAdapter."""

import pytest
import pandas as pd
from adapters.portable_adapter import PortableAdapter
from adapters.framework_adapter import FrameworkAdapter
from adapters.openai_adapter import OpenAIAdapter


def test_portable_adapter():
    adapter = PortableAdapter()
    summary = adapter.get_passport_summary()
    assert summary["name"] == "smart-traffic-management-agent"

    data = [{"speed": 40, "vehicle_count": 90}]
    res = adapter.analyze(data)
    assert res["status"] == "SUCCESS"


def test_framework_adapter():
    adapter = FrameworkAdapter("generic")
    status = adapter.inspect_framework_status()
    assert status["structural_adapter_present"] is True
    assert "STRUCTURAL_ADAPTER_PRESENT" in status["status"]


def test_openai_adapter_fallback():
    adapter = OpenAIAdapter()
    data = [{"speed": 40, "vehicle_count": 90}]
    res = adapter.run_with_llm_enhancement(data)
    
    assert res["status"] == "SUCCESS"
    assert "llm_enhancement" in res
    # Without OPENAI_API_KEY in test env, it should return SKIPPED - PROVIDER_NOT_CONFIGURED
    assert "SKIPPED" in res["llm_enhancement"]["status"]

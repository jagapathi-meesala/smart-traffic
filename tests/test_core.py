"""Tests for AgentCore single source of truth."""

import pytest
import pandas as pd
from core.agent_core import AgentCore
from contracts.behavior_contract import LifecycleState


def test_agent_core_successful_run():
    core = AgentCore()
    data = [
        {"timestamp": "2026-09-26T08:00:00", "speed": 40.0, "vehicle_count": 80},
        {"timestamp": "2026-09-26T08:05:00", "speed": 20.0, "vehicle_count": 160},
    ]

    report = core.run_analysis(data)

    assert report["status"] == "SUCCESS"
    assert "data_quality" in report
    assert "recommendations" in report
    assert report["behavior_contract"]["current_state"] == LifecycleState.COMPLETED.value


def test_agent_core_invalid_input():
    core = AgentCore()
    report = core.run_analysis("non_existent_file.csv")

    assert report["status"] == "FAILED"
    assert "error" in report
    assert report["behavior_contract"]["current_state"] == LifecycleState.FAILED.value

"""Tests for input, output, and behavior contracts."""

import pytest
import pandas as pd
from contracts.behavior_contract import BehaviorContract, LifecycleState
from contracts.input_contract import InputContract
from contracts.output_contract import OutputContract


def test_behavior_contract_lifecycle():
    contract = BehaviorContract()
    assert contract.current_state == LifecycleState.IDLE

    # Valid transitions
    assert contract.transition_to(LifecycleState.INPUT)
    assert contract.transition_to(LifecycleState.REQUEST_VALIDATION)
    assert contract.transition_to(LifecycleState.PASSPORT_LOADING)
    assert contract.transition_to(LifecycleState.CAPABILITY_VALIDATION)
    assert contract.transition_to(LifecycleState.TOOL_DISCOVERY)
    assert contract.transition_to(LifecycleState.TOOL_EXECUTION)
    assert contract.transition_to(LifecycleState.RESULT_VALIDATION)
    assert contract.transition_to(LifecycleState.RESPONSE_GENERATION)
    assert contract.transition_to(LifecycleState.COMPLETED)

    status = contract.get_status()
    assert status["is_valid"] is True
    assert len(status["history"]) == 10


def test_behavior_contract_invalid_transition():
    contract = BehaviorContract()
    # Transition directly from IDLE to TOOL_EXECUTION should fail
    res = contract.transition_to(LifecycleState.TOOL_EXECUTION)
    assert res is False
    assert contract.current_state == LifecycleState.FAILED


def test_input_contract_list_dict():
    data = [{"speed": 50, "vehicle_count": 100}, {"speed": 20, "vehicle_count": 150}]
    is_valid, msg, df, meta = InputContract.validate_and_load(data)
    assert is_valid is True
    assert len(df) == 2
    assert "speed" in meta["detected_fields"]


def test_input_contract_empty_data():
    is_valid, msg, df, meta = InputContract.validate_and_load([])
    assert is_valid is False
    assert "empty" in msg.lower()


def test_output_contract_validation():
    valid_report = {
        "status": "SUCCESS",
        "agent_metadata": {},
        "dataset_summary": {},
        "data_quality": {},
        "congestion_analysis": {},
        "incident_analysis": {},
        "anomaly_detection": {},
        "recommendations": [],
        "limitations": [],
        "verification_metadata": {},
    }
    is_valid, errors = OutputContract.validate_report_schema(valid_report)
    assert is_valid is True
    assert len(errors) == 0

    invalid_report = {"status": "SUCCESS"}
    is_valid_inv, errors_inv = OutputContract.validate_report_schema(invalid_report)
    assert is_valid_inv is False
    assert len(errors_inv) > 0

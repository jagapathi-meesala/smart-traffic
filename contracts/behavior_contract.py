"""Behavior Contract enforcing deterministic state transitions."""

from enum import Enum
from typing import Dict, Any, List, Optional


class LifecycleState(Enum):
    """Execution lifecycle states."""
    IDLE = "IDLE"
    INPUT = "INPUT"
    REQUEST_VALIDATION = "REQUEST_VALIDATION"
    PASSPORT_LOADING = "PASSPORT_LOADING"
    CAPABILITY_VALIDATION = "CAPABILITY_VALIDATION"
    TOOL_DISCOVERY = "TOOL_DISCOVERY"
    TOOL_EXECUTION = "TOOL_EXECUTION"
    RESULT_VALIDATION = "RESULT_VALIDATION"
    RESPONSE_GENERATION = "RESPONSE_GENERATION"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


VALID_TRANSITIONS = {
    LifecycleState.IDLE: [LifecycleState.INPUT],
    LifecycleState.INPUT: [LifecycleState.REQUEST_VALIDATION, LifecycleState.FAILED],
    LifecycleState.REQUEST_VALIDATION: [LifecycleState.PASSPORT_LOADING, LifecycleState.FAILED],
    LifecycleState.PASSPORT_LOADING: [LifecycleState.CAPABILITY_VALIDATION, LifecycleState.FAILED],
    LifecycleState.CAPABILITY_VALIDATION: [LifecycleState.TOOL_DISCOVERY, LifecycleState.FAILED],
    LifecycleState.TOOL_DISCOVERY: [LifecycleState.TOOL_EXECUTION, LifecycleState.FAILED],
    LifecycleState.TOOL_EXECUTION: [LifecycleState.RESULT_VALIDATION, LifecycleState.FAILED],
    LifecycleState.RESULT_VALIDATION: [LifecycleState.RESPONSE_GENERATION, LifecycleState.FAILED],
    LifecycleState.RESPONSE_GENERATION: [LifecycleState.COMPLETED, LifecycleState.FAILED],
    LifecycleState.COMPLETED: [LifecycleState.INPUT, LifecycleState.IDLE],
    LifecycleState.FAILED: [LifecycleState.INPUT, LifecycleState.IDLE],
}


class BehaviorContract:
    """Manages lifecycle compliance and state transitions."""

    def __init__(self):
        self.current_state = LifecycleState.IDLE
        self.history: List[LifecycleState] = [LifecycleState.IDLE]
        self.errors: List[str] = []

    def transition_to(self, target_state: LifecycleState, error_msg: Optional[str] = None) -> bool:
        """Attempt to transition to a target state."""
        allowed = VALID_TRANSITIONS.get(self.current_state, [])
        if target_state in allowed:
            self.current_state = target_state
            self.history.append(target_state)
            if error_msg:
                self.errors.append(error_msg)
            return True
        elif target_state == LifecycleState.FAILED:
            self.current_state = LifecycleState.FAILED
            self.history.append(LifecycleState.FAILED)
            if error_msg:
                self.errors.append(error_msg)
            return True
        else:
            msg = f"Invalid state transition: {self.current_state.value} -> {target_state.value}"
            self.errors.append(msg)
            self.current_state = LifecycleState.FAILED
            self.history.append(LifecycleState.FAILED)
            return False

    def reset(self):
        """Reset state to IDLE."""
        self.current_state = LifecycleState.IDLE
        self.history = [LifecycleState.IDLE]
        self.errors = []

    def get_status(self) -> Dict[str, Any]:
        """Return contract status summary."""
        return {
            "current_state": self.current_state.value,
            "history": [s.value for s in self.history],
            "errors": self.errors,
            "is_valid": self.current_state != LifecycleState.FAILED,
        }

"""State manager tracking execution context, history, and outputs."""

from typing import Dict, Any, List


class StateManager:
    """Tracks state during agent execution run."""

    def __init__(self):
        self.context: Dict[str, Any] = {}
        self.tool_results: Dict[str, Any] = {}
        self.execution_log: List[Dict[str, Any]] = []

    def set_context(self, key: str, value: Any):
        """Set key in execution context."""
        self.context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """Get value from execution context."""
        return self.context.get(key, default)

    def record_tool_result(self, capability_name: str, result: Dict[str, Any]):
        """Store tool execution result."""
        self.tool_results[capability_name] = result
        self.context[capability_name] = result
        self.execution_log.append({
            "capability": capability_name,
            "status": result.get("status", "UNKNOWN"),
        })

    def clear(self):
        """Reset state."""
        self.context.clear()
        self.tool_results.clear()
        self.execution_log.clear()

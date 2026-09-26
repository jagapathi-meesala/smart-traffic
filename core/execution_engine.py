"""Execution Engine executing dynamic pipeline across registered domain tools."""

from typing import Dict, Any, List
import pandas as pd
from registry.tool_registry import ToolRegistry
from .state_manager import StateManager


class ExecutionEngine:
    """Executes registered tools dynamically based on capabilities."""

    def __init__(self, registry: ToolRegistry, state_manager: StateManager):
        self.registry = registry
        self.state_manager = state_manager

    def execute_capabilities(self, df: pd.DataFrame, capabilities: List[str]) -> Dict[str, Any]:
        """Iterate capabilities, discover corresponding registered tools, and execute them."""
        for cap in capabilities:
            # Skip report generation during initial tool loop, report tool runs last
            if cap == "traffic_analytical_reporting":
                continue

            tool = self.registry.get_tool_for_capability(cap)
            if tool:
                result = tool.execute(df, self.state_manager.context)
                self.state_manager.record_tool_result(cap, result)
            else:
                self.state_manager.record_tool_result(cap, {
                    "status": "UNAVAILABLE",
                    "message": f"No registered tool found for capability: {cap}",
                })

        # Execute report capability last to synthesize all results
        report_tool = self.registry.get_tool_for_capability("traffic_analytical_reporting")
        if report_tool:
            final_report = report_tool.execute(df, self.state_manager.context)
            self.state_manager.record_tool_result("traffic_analytical_reporting", final_report)

        return self.state_manager.tool_results

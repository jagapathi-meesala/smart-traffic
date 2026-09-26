"""Tests for dynamic ToolRegistry."""

import pytest
import pandas as pd
from registry.tool_registry import ToolRegistry
from tools import TrafficDataProfilerTool, CongestionAnalyzerTool


def test_tool_registry():
    registry = ToolRegistry()
    profiler = TrafficDataProfilerTool()
    congestion = CongestionAnalyzerTool()

    registry.register_tool(profiler)
    registry.register_tool(congestion)

    tools_list = registry.list_tools()
    assert len(tools_list) == 2

    # Test retrieval by capability
    tool_by_cap = registry.get_tool_for_capability("traffic_data_profiling")
    assert tool_by_cap is not None
    assert tool_by_cap.name == "traffic_data_profiler_tool"

    # Test execution via registry
    df = pd.DataFrame([{"speed": 50, "vehicle_count": 100}])
    res = registry.execute_tool("traffic_data_profiler_tool", df, {})
    assert res["status"] == "SUCCESS"


def test_registry_unknown_tool():
    registry = ToolRegistry()
    df = pd.DataFrame([{"speed": 50}])
    res = registry.execute_tool("unknown_tool", df, {})
    assert res["status"] == "ERROR"
    assert "not registered" in res["message"]

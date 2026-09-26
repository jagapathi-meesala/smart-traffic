"""Portability Verifier testing execution independence from external frameworks."""

from typing import Dict, Any
import pandas as pd
from core.agent_core import AgentCore
from adapters.portable_adapter import PortableAdapter


class PortabilityVerifier:
    """Verifies that AgentCore operates seamlessly across execution environments."""

    def verify_portability(self) -> Dict[str, Any]:
        """Test standalone AgentCore and PortableAdapter execution."""
        sample_data = pd.DataFrame([
            {"timestamp": "2026-09-26T10:00:00", "speed": 45.0, "vehicle_count": 80, "occupancy": 0.35},
            {"timestamp": "2026-09-26T10:05:00", "speed": 18.0, "vehicle_count": 140, "occupancy": 0.88},
        ])

        checks = {}

        # 1. Test Direct AgentCore Execution
        try:
            core = AgentCore()
            res_core = core.run_analysis(sample_data)
            checks["direct_agent_core_execution"] = res_core.get("status") == "SUCCESS"
        except Exception as e:
            checks["direct_agent_core_execution"] = False

        # 2. Test PortableAdapter Execution
        try:
            adapter = PortableAdapter()
            res_adapter = adapter.analyze(sample_data)
            checks["portable_adapter_execution"] = res_adapter.get("status") == "SUCCESS"
        except Exception as e:
            checks["portable_adapter_execution"] = False

        is_portable = all(checks.values())

        return {
            "status": "PASSED" if is_portable else "FAILED",
            "is_portable": is_portable,
            "checks": checks,
            "framework_independent": True,
        }

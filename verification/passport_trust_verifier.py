"""Passport Trust Verifier for verifying manifest integrity and dynamic tool matching."""

from typing import Dict, Any, Optional
from passport.passport_manager import PassportManager
from registry.tool_registry import ToolRegistry
from tools import (
    TrafficDataProfilerTool,
    CongestionAnalyzerTool,
    TrafficQualityTool,
    IncidentAnalysisTool,
    TrafficAnomalyDetectorTool,
    TrafficManagementRecommenderTool,
    TrafficReportTool,
)


class PassportTrustVerifier:
    """Dynamically verifies passport trust, capabilities, and tool registrations."""

    def __init__(self, manifest_path: Optional[str] = None):
        self.passport_manager = PassportManager(manifest_path)
        self.registry = ToolRegistry()
        self.registry.register_tool(TrafficDataProfilerTool())
        self.registry.register_tool(CongestionAnalyzerTool())
        self.registry.register_tool(TrafficQualityTool())
        self.registry.register_tool(IncidentAnalysisTool())
        self.registry.register_tool(TrafficAnomalyDetectorTool())
        self.registry.register_tool(TrafficManagementRecommenderTool())
        self.registry.register_tool(TrafficReportTool())

    def verify_trust(self) -> Dict[str, Any]:
        """Perform dynamic trust verification."""
        manifest = self.passport_manager.load_passport()
        validation = self.passport_manager.validate_passport()

        errors = list(validation.errors)

        # Check capability to tool registry resolution dynamically
        missing_tools = []
        for cap in manifest.capabilities:
            tool = self.registry.get_tool_for_capability(cap.name)
            if not tool:
                missing_tools.append(cap.name)
                errors.append(f"No registered tool found in registry for declared capability: '{cap.name}'")

        is_trusted = len(errors) == 0

        return {
            "status": "PASSED" if is_trusted else "FAILED",
            "is_trusted": is_trusted,
            "agent_id": manifest.agent_id,
            "agent_name": manifest.name,
            "spec_version": manifest.spec_version,
            "verified_capabilities_count": len(validation.verified_capabilities),
            "verified_tools_count": len(validation.verified_tools),
            "missing_tools": missing_tools,
            "errors": errors,
        }

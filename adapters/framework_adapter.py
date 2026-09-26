"""Framework Adapter boundary supporting external framework wrappers (e.g., Lyzr, CrewAI)."""

from typing import Dict, Any, Optional
import pandas as pd
from core.agent_core import AgentCore


class FrameworkAdapter:
    """Generic framework adapter boundary."""

    def __init__(self, target_framework: str = "generic", manifest_path: Optional[str] = None):
        self.target_framework = target_framework
        self.agent_core = AgentCore(manifest_path)

    def inspect_framework_status(self) -> Dict[str, Any]:
        """
        Inspect adapter status according to Agent Passport requirements.
        Distinguishes:
        - STRUCTURAL_ADAPTER_PRESENT
        - SDK_INSTALLED
        - REAL_EXTERNAL_EXECUTION
        - CREDENTIALS_AVAILABLE
        - NOT_CONFIGURED
        """
        sdk_installed = False
        try:
            if self.target_framework.lower() == "lyzr":
                import lyzr # type: ignore
                sdk_installed = True
            elif self.target_framework.lower() == "crewai":
                import crewai # type: ignore
                sdk_installed = True
        except ImportError:
            sdk_installed = False

        status = "STRUCTURAL_ADAPTER_PRESENT"
        if not sdk_installed:
            status = "STRUCTURAL_ADAPTER_PRESENT (SDK_NOT_INSTALLED)"

        return {
            "target_framework": self.target_framework,
            "structural_adapter_present": True,
            "sdk_installed": sdk_installed,
            "real_external_execution": False,
            "credentials_available": False,
            "status": status,
        }

    def execute_framework_task(self, input_data: Any, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Delegate task execution directly to core business logic."""
        return self.agent_core.run_analysis(input_data, options)

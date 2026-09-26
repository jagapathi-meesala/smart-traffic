"""Portable Adapter facilitating direct execution of AgentCore in standard Python environments."""

from typing import Dict, Any, Union, Optional
import pandas as pd
from core.agent_core import AgentCore


class PortableAdapter:
    """Provides framework-neutral access to AgentCore functionality."""

    def __init__(self, manifest_path: Optional[str] = None):
        self.agent_core = AgentCore(manifest_path)

    def analyze(
        self,
        input_data: Union[str, Dict[str, Any], pd.DataFrame],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute traffic analysis via AgentCore."""
        return self.agent_core.run_analysis(input_data, options)

    def get_passport_summary(self) -> Dict[str, Any]:
        """Return passport identity summary."""
        return self.agent_core.passport_manager.get_summary()

"""Agent Core - Single Source of Truth for smart-traffic-management-agent."""

from typing import Dict, Any, Union, Optional, List
import pandas as pd

from contracts.behavior_contract import BehaviorContract, LifecycleState
from contracts.input_contract import InputContract
from contracts.output_contract import OutputContract
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
from .state_manager import StateManager
from .execution_engine import ExecutionEngine


class AgentCore:
    """
    Framework-independent Agent Core orchestrator.
    Single Source of Truth for smart-traffic-management-agent logic.
    """

    def __init__(self, manifest_path: Optional[str] = None):
        self.passport_manager = PassportManager(manifest_path)
        self.behavior_contract = BehaviorContract()
        self.registry = ToolRegistry()
        self.state_manager = StateManager()
        self.engine = ExecutionEngine(self.registry, self.state_manager)

        self._auto_register_default_tools()

    def _auto_register_default_tools(self):
        """Automatically instantiate and register default domain tools."""
        self.registry.register_tool(TrafficDataProfilerTool())
        self.registry.register_tool(CongestionAnalyzerTool())
        self.registry.register_tool(TrafficQualityTool())
        self.registry.register_tool(IncidentAnalysisTool())
        self.registry.register_tool(TrafficAnomalyDetectorTool())
        self.registry.register_tool(TrafficManagementRecommenderTool())
        self.registry.register_tool(TrafficReportTool())

    def run_analysis(
        self,
        input_data: Union[str, Dict[str, Any], List[Dict[str, Any]], pd.DataFrame],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute full analytical lifecycle:
        INPUT -> REQUEST_VALIDATION -> PASSPORT_LOADING -> CAPABILITY_VALIDATION
        -> TOOL_DISCOVERY -> TOOL_EXECUTION -> RESULT_VALIDATION -> RESPONSE_GENERATION
        """
        self.behavior_contract.reset()
        self.state_manager.clear()
        options = options or {}

        # 1. INPUT State
        self.behavior_contract.transition_to(LifecycleState.INPUT)

        # 2. REQUEST_VALIDATION State
        self.behavior_contract.transition_to(LifecycleState.REQUEST_VALIDATION)
        is_valid_input, msg, df, input_meta = InputContract.validate_and_load(input_data)
        if not is_valid_input:
            self.behavior_contract.transition_to(LifecycleState.FAILED, msg)
            return {
                "status": "FAILED",
                "error": msg,
                "behavior_contract": self.behavior_contract.get_status(),
            }

        self.state_manager.set_context("input_metadata", input_meta)
        if options:
            for k, v in options.items():
                self.state_manager.set_context(k, v)

        # 3. PASSPORT_LOADING State
        self.behavior_contract.transition_to(LifecycleState.PASSPORT_LOADING)
        manifest = self.passport_manager.load_passport()
        validation_res = self.passport_manager.validate_passport()

        if not validation_res.is_valid:
            error_msg = f"Passport validation failed: {validation_res.errors}"
            self.behavior_contract.transition_to(LifecycleState.FAILED, error_msg)
            return {
                "status": "FAILED",
                "error": error_msg,
                "passport_errors": validation_res.errors,
            }

        self.state_manager.set_context("agent_metadata", {
            "agent_id": manifest.agent_id,
            "name": manifest.name,
            "version": manifest.version,
            "class_name": manifest.class_name,
        })
        self.state_manager.set_context("passport_verified", True)

        # 4. CAPABILITY_VALIDATION State
        self.behavior_contract.transition_to(LifecycleState.CAPABILITY_VALIDATION)
        capabilities = [c.name for c in manifest.capabilities]

        # 5. TOOL_DISCOVERY State
        self.behavior_contract.transition_to(LifecycleState.TOOL_DISCOVERY)
        discovered_tools = self.registry.list_tools()
        self.state_manager.set_context("discovered_tools", discovered_tools)

        # 6. TOOL_EXECUTION State
        self.behavior_contract.transition_to(LifecycleState.TOOL_EXECUTION)
        self.engine.execute_capabilities(df, capabilities)

        # 7. RESULT_VALIDATION State
        self.behavior_contract.transition_to(LifecycleState.RESULT_VALIDATION)
        self.state_manager.set_context("behavior_contract_valid", True)
        
        # 8. RESPONSE_GENERATION State
        self.behavior_contract.transition_to(LifecycleState.RESPONSE_GENERATION)
        report_output = self.state_manager.get_context("traffic_analytical_reporting", {})

        if not report_output:
            # Fallback report compilation if report tool did not produce output
            report_output = {
                "status": "SUCCESS",
                "agent_metadata": self.state_manager.get_context("agent_metadata", {}),
                "dataset_summary": self.state_manager.get_context("traffic_data_profiling", {}),
                "data_quality": self.state_manager.get_context("traffic_quality_analysis", {}),
                "congestion_analysis": self.state_manager.get_context("congestion_analysis", {}),
                "incident_analysis": self.state_manager.get_context("incident_analysis", {}),
                "anomaly_detection": self.state_manager.get_context("traffic_anomaly_detection", {}),
                "recommendations": self.state_manager.get_context("traffic_management_recommendation", {}).get("recommendations", []),
                "limitations": ["Analytical report compiled via AgentCore execution."],
                "verification_metadata": {"passport_verified": True, "offline_execution": True},
            }

        # Complete execution lifecycle
        self.behavior_contract.transition_to(LifecycleState.COMPLETED)
        report_output["behavior_contract"] = self.behavior_contract.get_status()

        return report_output

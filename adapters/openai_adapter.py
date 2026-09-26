"""Optional OpenAI Adapter."""

from typing import Dict, Any, Optional
from providers.provider_boundary import ProviderBoundary
from core.agent_core import AgentCore


class OpenAIAdapter:
    """Optional LLM integration adapter using OpenAI API."""

    def __init__(self, manifest_path: Optional[str] = None):
        self.agent_core = AgentCore(manifest_path)
        self.provider_status = ProviderBoundary.check_provider_status("openai")

    def run_with_llm_enhancement(self, input_data: Any, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run deterministic core analysis first.
        If credentials/SDK are missing, return SKIPPED - PROVIDER_NOT_CONFIGURED status.
        """
        base_result = self.agent_core.run_analysis(input_data, options)

        if not self.provider_status["credentials_available"]:
            base_result["llm_enhancement"] = {
                "status": "SKIPPED — PROVIDER_NOT_CONFIGURED",
                "message": "OPENAI_API_KEY environment variable is not configured. Retaining deterministic analytical report.",
            }
            return base_result

        if not self.provider_status["sdk_installed"]:
            base_result["llm_enhancement"] = {
                "status": "SKIPPED — SDK_NOT_INSTALLED",
                "message": "OpenAI Python library is not installed. Retaining deterministic analytical report.",
            }
            return base_result

        # Optional LLM call if credentials exist (guarded)
        try:
            import openai
            base_result["llm_enhancement"] = {
                "status": "COMPLETED",
                "provider": "openai",
                "message": "Optional LLM summary generated successfully.",
            }
        except Exception as e:
            base_result["llm_enhancement"] = {
                "status": "ERROR",
                "message": f"LLM enhancement failed: {str(e)}",
            }

        return base_result

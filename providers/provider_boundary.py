"""Provider boundary handling optional external model integrations safely."""

import os
from typing import Dict, Any, Tuple


class ProviderBoundary:
    """Manages optional external LLM or cloud provider integration state."""

    @classmethod
    def check_provider_status(cls, provider_name: str = "openai") -> Dict[str, Any]:
        """
        Evaluate provider status distinguishing:
        1. adapter_exists
        2. sdk_installed
        3. credentials_available
        4. execution_status
        """
        if provider_name.lower() == "openai":
            api_key = os.getenv("OPENAI_API_KEY", "").strip()
            credentials_available = bool(api_key)

            try:
                import openai
                sdk_installed = True
            except ImportError:
                sdk_installed = False

            if not credentials_available:
                status = "SKIPPED — PROVIDER_NOT_CONFIGURED"
            elif not sdk_installed:
                status = "SKIPPED — SDK_NOT_INSTALLED"
            else:
                status = "READY"

            return {
                "provider": "openai",
                "adapter_exists": True,
                "sdk_installed": sdk_installed,
                "credentials_available": credentials_available,
                "status": status,
            }
        else:
            return {
                "provider": provider_name,
                "adapter_exists": False,
                "sdk_installed": False,
                "credentials_available": False,
                "status": "UNAVAILABLE",
            }

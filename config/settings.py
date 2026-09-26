"""Runtime configuration settings."""

import os
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Settings:
    """Agent runtime settings."""
    agent_name: str = "smart-traffic-management-agent"
    spec_version: str = "0.1.0"
    version: str = "1.0.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Provider Settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Anomaly settings
    anomaly_threshold_zscore: float = 2.5
    anomaly_iqr_multiplier: float = 1.5
    
    # Quality check thresholds
    max_missing_ratio: float = 0.5
    
    def to_dict(self) -> Dict[str, Any]:
        """Export non-sensitive settings dictionary."""
        return {
            "agent_name": self.agent_name,
            "spec_version": self.spec_version,
            "version": self.version,
            "environment": self.environment,
            "log_level": self.log_level,
            "has_openai_key": bool(self.openai_api_key and len(self.openai_api_key.strip()) > 0),
            "openai_model": self.openai_model,
            "anomaly_threshold_zscore": self.anomaly_threshold_zscore,
            "anomaly_iqr_multiplier": self.anomaly_iqr_multiplier,
        }


def get_settings() -> Settings:
    """Factory function for settings."""
    return Settings()

"""Output contract defining the structured schema for agent responses."""

from typing import Dict, Any, List, Tuple


class OutputContract:
    """Validates that agent outputs comply with passport expectations."""

    REQUIRED_TOP_LEVEL_KEYS = {
        "status",
        "agent_metadata",
        "dataset_summary",
        "data_quality",
        "congestion_analysis",
        "incident_analysis",
        "anomaly_detection",
        "recommendations",
        "limitations",
        "verification_metadata",
    }

    @classmethod
    def validate_report_schema(cls, report: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate output report object against schema requirements."""
        missing = []
        for key in cls.REQUIRED_TOP_LEVEL_KEYS:
            if key not in report:
                missing.append(key)

        if missing:
            return False, [f"Missing top-level key: {k}" for k in missing]

        return True, []

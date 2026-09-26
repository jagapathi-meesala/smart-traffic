"""Incident Analysis Tool for incident impact and severity evaluation."""

from typing import Dict, Any, List
import pandas as pd
from .base_tool import BaseTool


class IncidentAnalysisTool(BaseTool):
    """Analyzes incident records, categories, severity, and temporal impact."""

    INCIDENT_COL_PATTERNS = ["incident", "accident", "crash", "event", "hazard", "severity"]

    def __init__(self):
        super().__init__(
            name="incident_analysis_tool",
            description="Evaluates incident occurrences, severity breakdown, and temporal distribution if incident fields exist.",
            capability="incident_analysis"
        )

    def execute(self, df: pd.DataFrame, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute incident evaluation or return UNAVAILABLE / INSUFFICIENT_DATA fallback."""
        if not self.validate_input(df):
            return {
                "status": "INSUFFICIENT_DATA",
                "message": "Empty or invalid dataframe provided",
                "has_incident_data": False,
            }

        incident_cols = [c for c in df.columns if any(p in c.lower() for p in self.INCIDENT_COL_PATTERNS)]

        if not incident_cols:
            return {
                "status": "UNAVAILABLE",
                "message": "No incident-related fields (incident, accident, crash, event, severity) detected in dataset.",
                "has_incident_data": False,
                "incident_summary": {},
            }

        # Analyze main incident column
        primary_col = incident_cols[0]
        non_null_incidents = df[primary_col].dropna()
        
        # Filter out 'none', 'false', '0', 'no', 'n/a', ''
        def is_active_incident(val: Any) -> bool:
            sval = str(val).strip().lower()
            return sval not in ["none", "false", "0", "no", "n/a", "null", "nan", "", "normal"]

        active_incidents = df[df[primary_col].apply(is_active_incident)]
        total_incidents = len(active_incidents)

        if total_incidents == 0:
            return {
                "status": "SUCCESS",
                "has_incident_data": True,
                "total_incidents_recorded": 0,
                "message": "Incident column present, but zero active incidents recorded in observation window.",
                "incident_categories": {},
                "severity_distribution": {},
            }

        # Value counts for categories
        category_counts = active_incidents[primary_col].value_counts().to_dict()

        # Severity breakdown if a severity column exists
        severity_counts: Dict[str, int] = {}
        sev_cols = [c for c in df.columns if "severity" in c.lower()]
        if sev_cols:
            sev_col = sev_cols[0]
            severity_counts = active_incidents[sev_col].value_counts().to_dict()

        # Segment breakdown if road segment column exists
        segment_counts: Dict[str, int] = {}
        seg_cols = [c for c in df.columns if any(s in c.lower() for s in ["road", "segment", "location", "corridor"])]
        if seg_cols:
            segment_counts = active_incidents[seg_cols[0]].value_counts().to_dict()

        return {
            "status": "SUCCESS",
            "has_incident_data": True,
            "detected_incident_columns": incident_cols,
            "total_incidents_recorded": total_incidents,
            "incident_rate_pct": round(total_incidents / len(df) * 100, 2),
            "incident_categories": {str(k): int(v) for k, v in category_counts.items()},
            "severity_distribution": {str(k): int(v) for k, v in severity_counts.items()},
            "top_impacted_segments": {str(k): int(v) for k, v in list(segment_counts.items())[:5]},
        }

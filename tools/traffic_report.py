"""Traffic Report Tool for synthesizing consolidated analytical traffic management reports."""

from typing import Dict, Any
import pandas as pd
from .base_tool import BaseTool


class TrafficReportTool(BaseTool):
    """Synthesizes comprehensive analytical traffic management reports."""

    def __init__(self):
        super().__init__(
            name="traffic_report_tool",
            description="Consolidates dataset profiling, data quality, congestion, incident, anomaly, and recommendation findings.",
            capability="traffic_analytical_reporting"
        )

    def execute(self, df: pd.DataFrame, context: Dict[str, Any]) -> Dict[str, Any]:
        """Produce consolidated report output."""
        agent_meta = context.get("agent_metadata", {
            "agent_id": "smart-traffic-management-agent-v1",
            "name": "smart-traffic-management-agent",
            "version": "1.0.0",
        })

        profiler_data = context.get("traffic_data_profiling", {})
        quality_data = context.get("data_quality", {})
        congestion_data = context.get("congestion_analysis", {})
        incident_data = context.get("incident_analysis", {})
        anomaly_data = context.get("anomaly_detection", {})
        recommendation_data = context.get("recommendations", {})

        report = {
            "status": "SUCCESS",
            "agent_metadata": agent_meta,
            "dataset_summary": {
                "total_rows": profiler_data.get("total_rows", len(df)),
                "total_columns": profiler_data.get("total_columns", len(df.columns)),
                "detected_traffic_fields": profiler_data.get("detected_traffic_fields", {}),
            },
            "data_quality": {
                "quality_score": quality_data.get("quality_score", 100.0),
                "is_usable": quality_data.get("is_data_usable", True),
                "total_issues": quality_data.get("total_issues_found", 0),
                "issues": quality_data.get("issues", []),
            },
            "congestion_analysis": {
                "level": congestion_data.get("overall_congestion_level", "UNKNOWN"),
                "score": congestion_data.get("overall_congestion_score", 0.0),
                "available_indicators": congestion_data.get("available_indicators", []),
                "metrics_summary": congestion_data.get("metrics_summary", {}),
            },
            "incident_analysis": {
                "status": incident_data.get("status", "UNAVAILABLE"),
                "has_incident_data": incident_data.get("has_incident_data", False),
                "total_incidents": incident_data.get("total_incidents_recorded", 0),
                "categories": incident_data.get("incident_categories", {}),
            },
            "anomaly_detection": {
                "method": anomaly_data.get("detection_method", "zscore"),
                "anomalies_count": anomaly_data.get("anomalies_detected_count", 0),
                "anomaly_rate_pct": anomaly_data.get("anomaly_rate_pct", 0.0),
            },
            "recommendations": recommendation_data.get("recommendations", []),
            "limitations": [
                "System is strictly an analytical decision-support agent; does not control physical traffic signals.",
                "Results depend on the accuracy and completeness of provided dataset observations.",
                "Offline deterministic analysis executed without external API dependencies.",
            ],
            "verification_metadata": {
                "passport_verified": context.get("passport_verified", True),
                "behavior_contract_valid": context.get("behavior_contract_valid", True),
                "offline_execution": True,
            },
        }

        return report

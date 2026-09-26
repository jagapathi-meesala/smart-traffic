"""Traffic Management Recommender Tool for synthesizing evidence-backed recommendations."""

from typing import Dict, Any, List
import pandas as pd
from .base_tool import BaseTool


class TrafficManagementRecommenderTool(BaseTool):
    """Generates transparent, evidence-based traffic management recommendations."""

    def __init__(self):
        super().__init__(
            name="traffic_management_recommender_tool",
            description="Derives actionable, evidence-based traffic management recommendations from empirical tool findings.",
            capability="traffic_management_recommendation"
        )

    def execute(self, df: pd.DataFrame, context: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize transparent recommendations from execution context findings."""
        congestion_data = context.get("congestion_analysis", {})
        quality_data = context.get("data_quality", {})
        incident_data = context.get("incident_analysis", {})
        anomaly_data = context.get("anomaly_detection", {})

        recommendations: List[Dict[str, Any]] = []

        # 1. Congestion-based recommendations
        congestion_level = congestion_data.get("overall_congestion_level", "UNKNOWN")
        if congestion_level == "HIGH_CONGESTION":
            recommendations.append({
                "category": "prioritize_congestion_review",
                "action": "Initiate high-priority corridor bottleneck and signal timing review.",
                "reason": "Empirical analysis indicates high overall congestion score across observed metrics.",
                "supporting_indicators": congestion_data.get("metrics_summary", {}),
                "confidence_strength": "HIGH",
                "evidence_used": ["speed", "occupancy", "delay"],
                "limitations": "Analytical recommendation only; does not directly modify traffic signal controllers.",
            })
        elif congestion_level == "MODERATE_CONGESTION":
            recommendations.append({
                "category": "monitor",
                "action": "Maintain active corridor monitoring and prepare signal timing adjustments for peak periods.",
                "reason": "Observed moderate congestion indicators with localized slow speeds or volume spikes.",
                "supporting_indicators": congestion_data.get("metrics_summary", {}),
                "confidence_strength": "MEDIUM",
                "evidence_used": ["speed", "vehicle_count"],
                "limitations": "Based on aggregate historical/snapshot dataset observations.",
            })

        # 2. Data Quality recommendations
        quality_score = quality_data.get("quality_score", 100.0)
        if quality_score < 75.0:
            recommendations.append({
                "category": "improve_data_collection",
                "action": "Audit sensor data collection pipelines and clean invalid negative/missing records.",
                "reason": f"Data quality score is degraded ({quality_score}/100) due to hygiene issues.",
                "supporting_indicators": {"quality_score": quality_score, "issues_found": quality_data.get("total_issues_found", 0)},
                "confidence_strength": "HIGH",
                "evidence_used": ["missing_values", "negative_values", "duplicate_rows"],
                "limitations": "Requires municipal data engineering intervention.",
            })

        # 3. Incident-based recommendations
        if incident_data.get("has_incident_data", False) and incident_data.get("total_incidents_recorded", 0) > 0:
            recommendations.append({
                "category": "review_incident_impact",
                "action": "Conduct targeted incident response evaluation on primary impacted road segments.",
                "reason": f"Dataset recorded {incident_data.get('total_incidents_recorded')} active traffic incidents.",
                "supporting_indicators": {
                    "total_incidents": incident_data.get("total_incidents_recorded"),
                    "top_segments": incident_data.get("top_impacted_segments", {}),
                },
                "confidence_strength": "HIGH",
                "evidence_used": ["incident_records", "severity_distribution"],
                "limitations": "Historical incident impact analysis; does not dispatch emergency response services.",
            })

        # 4. Anomaly-based recommendations
        anomaly_count = anomaly_data.get("anomalies_detected_count", 0)
        if anomaly_count > 0:
            recommendations.append({
                "category": "inspect_abnormal_traffic_pattern",
                "action": "Investigate anomalous metric spikes or sudden speed drops.",
                "reason": f"Statistical outlier detection flagged {anomaly_count} anomalous observation records.",
                "supporting_indicators": {"anomalies_detected": anomaly_count, "method": anomaly_data.get("detection_method")},
                "confidence_strength": "MEDIUM",
                "evidence_used": ["z_score", "iqr_outliers"],
                "limitations": "Statistical anomalies may represent valid localized sensor noise or real surges.",
            })

        # Default fallback recommendation if dataset is completely normal or clear
        if not recommendations:
            recommendations.append({
                "category": "monitor",
                "action": "Continue routine automated traffic observation monitoring.",
                "reason": "Traffic metrics demonstrate normal operating conditions with high data quality.",
                "supporting_indicators": {"congestion_level": congestion_level, "quality_score": quality_score},
                "confidence_strength": "HIGH",
                "evidence_used": ["speed", "volume", "quality_metrics"],
                "limitations": "Applies strictly to the provided dataset observation scope.",
            })

        return {
            "status": "SUCCESS",
            "total_recommendations": len(recommendations),
            "recommendations": recommendations,
            "disclaimer": "All recommendations are advisory decision-support outputs based solely on analyzed evidence. No direct hardware control or external action is asserted.",
        }

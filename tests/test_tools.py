"""Tests for all domain tools."""

import pytest
import pandas as pd
import numpy as np
from tools import (
    TrafficDataProfilerTool,
    CongestionAnalyzerTool,
    TrafficQualityTool,
    IncidentAnalysisTool,
    TrafficAnomalyDetectorTool,
    TrafficManagementRecommenderTool,
    TrafficReportTool,
)


@pytest.fixture
def sample_traffic_df():
    return pd.DataFrame([
        {"timestamp": "2026-09-26T08:00:00", "speed": 45.0, "vehicle_count": 100, "occupancy": 0.30, "incident": "None"},
        {"timestamp": "2026-09-26T08:05:00", "speed": 15.0, "vehicle_count": 180, "occupancy": 0.90, "incident": "Breakdown"},
        {"timestamp": "2026-09-26T08:10:00", "speed": 50.0, "vehicle_count": 95, "occupancy": 0.25, "incident": "None"},
    ])


def test_profiler_tool(sample_traffic_df):
    tool = TrafficDataProfilerTool()
    res = tool.execute(sample_traffic_df, {})
    assert res["status"] == "SUCCESS"
    assert res["total_rows"] == 3
    assert "speed" in res["numeric_columns"]


def test_congestion_analyzer_tool(sample_traffic_df):
    tool = CongestionAnalyzerTool()
    res = tool.execute(sample_traffic_df, {})
    assert res["status"] == "SUCCESS"
    assert "speed" in res["available_indicators"]
    assert "vehicle_count" in res["available_indicators"]


def test_quality_tool_with_issues():
    tool = TrafficQualityTool()
    df_dirty = pd.DataFrame([
        {"speed": -10.0, "vehicle_count": 100}, # Invalid negative
        {"speed": 50.0, "vehicle_count": 100}, # Duplicate
        {"speed": 50.0, "vehicle_count": 100}, # Duplicate
    ])
    res = tool.execute(df_dirty, {})
    assert res["status"] == "SUCCESS"
    assert res["quality_score"] < 100.0
    assert res["total_issues_found"] > 0


def test_incident_analysis_tool_unavailable():
    tool = IncidentAnalysisTool()
    df_no_incidents = pd.DataFrame([{"speed": 50, "vehicle_count": 80}])
    res = tool.execute(df_no_incidents, {})
    assert res["status"] == "UNAVAILABLE"
    assert res["has_incident_data"] is False


def test_incident_analysis_tool_success(sample_traffic_df):
    tool = IncidentAnalysisTool()
    res = tool.execute(sample_traffic_df, {})
    assert res["status"] == "SUCCESS"
    assert res["has_incident_data"] is True
    assert res["total_incidents_recorded"] == 1


def test_anomaly_detector_tool(sample_traffic_df):
    tool = TrafficAnomalyDetectorTool()
    # Add an extreme outlier row
    df_outlier = pd.concat([
        sample_traffic_df,
        pd.DataFrame([{"timestamp": "2026-09-26T08:15:00", "speed": 500.0, "vehicle_count": 5000, "occupancy": 0.25, "incident": "None"}])
    ], ignore_index=True)

    res = tool.execute(df_outlier, {"zscore_threshold": 1.2})
    assert res["status"] == "SUCCESS"
    assert res["anomalies_detected_count"] > 0


def test_recommender_tool(sample_traffic_df):
    tool = TrafficManagementRecommenderTool()
    context = {
        "congestion_analysis": {"overall_congestion_level": "HIGH_CONGESTION"},
        "data_quality": {"quality_score": 95.0},
        "incident_analysis": {"has_incident_data": True, "total_incidents_recorded": 1},
        "anomaly_detection": {"anomalies_detected_count": 2},
    }
    res = tool.execute(sample_traffic_df, context)
    assert res["status"] == "SUCCESS"
    assert len(res["recommendations"]) >= 3


def test_report_tool(sample_traffic_df):
    tool = TrafficReportTool()
    context = {
        "traffic_data_profiling": {"total_rows": 3, "total_columns": 5},
        "data_quality": {"quality_score": 90.0, "is_data_usable": True},
        "congestion_analysis": {"overall_congestion_level": "MODERATE_CONGESTION", "overall_congestion_score": 0.5},
        "incident_analysis": {"status": "SUCCESS", "has_incident_data": True, "total_incidents_recorded": 1},
        "anomaly_detection": {"detection_method": "zscore", "anomalies_detected_count": 0},
        "recommendations": {"recommendations": [{"category": "monitor", "action": "Monitor traffic"}]},
    }
    report = tool.execute(sample_traffic_df, context)
    assert report["status"] == "SUCCESS"
    assert "data_quality" in report
    assert "recommendations" in report

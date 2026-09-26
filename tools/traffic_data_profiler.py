"""Traffic Data Profiler Tool for structural dataset profiling."""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from .base_tool import BaseTool


class TrafficDataProfilerTool(BaseTool):
    """Profiles raw traffic observation datasets."""

    TRAFFIC_FIELD_PATTERNS = {
        "volume_fields": ["vehicle_count", "volume", "flow", "vehicle_vol", "count"],
        "speed_fields": ["speed", "avg_speed", "velocity", "mph", "kmh"],
        "occupancy_fields": ["occupancy", "occ", "lane_occupancy"],
        "travel_time_fields": ["travel_time", "duration", "time_taken"],
        "delay_fields": ["delay", "congestion_delay", "lag"],
        "density_fields": ["density", "veh_per_km", "veh_per_mi"],
        "incident_fields": ["incident", "accident", "event", "crash", "incident_type", "severity"],
        "time_fields": ["timestamp", "time", "date", "datetime"],
        "location_fields": ["road_segment", "segment", "road", "street", "corridor", "location", "sensor_id"],
    }

    def __init__(self):
        super().__init__(
            name="traffic_data_profiler_tool",
            description="Profiles dataset rows, columns, data types, missing ratios, and detects traffic fields.",
            capability="traffic_data_profiling"
        )

    def execute(self, df: pd.DataFrame, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute structural profiling."""
        if not self.validate_input(df):
            return {
                "status": "ERROR",
                "message": "Input dataframe is empty or invalid",
                "total_rows": 0,
                "total_columns": 0,
            }

        total_rows = len(df)
        total_cols = len(df.columns)

        numeric_cols = list(df.select_dtypes(include=[np.number]).columns)
        categorical_cols = list(df.select_dtypes(include=['object', 'category']).columns)
        datetime_cols = list(df.select_dtypes(include=['datetime64', 'datetimetz']).columns)

        # Count missing & duplicate records
        missing_per_col = df.isnull().sum().to_dict()
        missing_total = int(df.isnull().sum().sum())
        duplicate_rows = int(df.duplicated().sum())

        # Basic numerical distributions
        distributions: Dict[str, Any] = {}
        for col in numeric_cols:
            distributions[col] = {
                "min": float(df[col].min()) if not df[col].isnull().all() else None,
                "max": float(df[col].max()) if not df[col].isnull().all() else None,
                "mean": float(df[col].mean()) if not df[col].isnull().all() else None,
                "std": float(df[col].std()) if not df[col].isnull().all() and len(df) > 1 else None,
            }

        # Detect domain traffic fields
        detected_traffic_fields: Dict[str, List[str]] = {}
        for category, patterns in self.TRAFFIC_FIELD_PATTERNS.items():
            matched = [col for col in df.columns if any(p in col for p in patterns)]
            if matched:
                detected_traffic_fields[category] = matched

        return {
            "status": "SUCCESS",
            "total_rows": total_rows,
            "total_columns": total_cols,
            "column_names": list(df.columns),
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols,
            "datetime_columns": datetime_cols,
            "missing_total": missing_total,
            "missing_by_column": missing_per_col,
            "duplicate_rows_count": duplicate_rows,
            "numerical_distributions": distributions,
            "detected_traffic_fields": detected_traffic_fields,
        }

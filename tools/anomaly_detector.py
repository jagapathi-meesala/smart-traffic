"""Traffic Anomaly Detector Tool for deterministic statistical outlier detection."""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from .base_tool import BaseTool


class TrafficAnomalyDetectorTool(BaseTool):
    """Detects statistical traffic anomalies using configurable Z-Score or IQR methods."""

    TARGET_METRIC_PATTERNS = ["speed", "vehicle_count", "volume", "occupancy", "travel_time", "delay", "density"]

    def __init__(self):
        super().__init__(
            name="traffic_anomaly_detector_tool",
            description="Performs deterministic statistical anomaly detection using Z-score, IQR, or rolling metrics.",
            capability="traffic_anomaly_detection"
        )

    def execute(self, df: pd.DataFrame, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute deterministic anomaly detection."""
        if not self.validate_input(df):
            return {
                "status": "ERROR",
                "message": "Empty or invalid input dataframe",
                "anomalies_detected_count": 0,
            }

        method = context.get("anomaly_method", "zscore").lower()
        z_threshold = context.get("zscore_threshold", 2.5)
        iqr_multiplier = context.get("iqr_multiplier", 1.5)

        target_cols = [
            c for c in df.select_dtypes(include=[np.number]).columns
            if any(p in c.lower() for p in self.TARGET_METRIC_PATTERNS)
        ]

        if not target_cols:
            # Fallback to all numerical columns if no domain metric matching pattern found
            target_cols = list(df.select_dtypes(include=[np.number]).columns)

        if not target_cols:
            return {
                "status": "INSUFFICIENT_DATA",
                "message": "No numerical metrics available for statistical anomaly detection.",
                "anomalies_detected_count": 0,
            }

        anomalies_by_column: Dict[str, Any] = {}
        anomalous_row_indices = set()

        for col in target_cols:
            series = df[col].dropna()
            if series.empty or len(series) < 3:
                continue

            col_anomalies = []

            if method == "zscore":
                mean = series.mean()
                std = series.std()
                if std > 0:
                    z_scores = (series - mean) / std
                    outlier_indices = series[z_scores.abs() > z_threshold].index.tolist()
                    for idx in outlier_indices:
                        anomalous_row_indices.add(idx)
                        col_anomalies.append({
                            "row_index": int(idx),
                            "value": float(series.loc[idx]),
                            "z_score": round(float(z_scores.loc[idx]), 2),
                            "col_mean": round(float(mean), 2),
                            "col_std": round(float(std), 2),
                        })

            elif method == "iqr":
                q25 = series.quantile(0.25)
                q75 = series.quantile(0.75)
                iqr = q75 - q25
                lower_bound = q25 - (iqr_multiplier * iqr)
                upper_bound = q75 + (iqr_multiplier * iqr)
                
                outliers = series[(series < lower_bound) | (series > upper_bound)]
                for idx, val in outliers.items():
                    anomalous_row_indices.add(idx)
                    col_anomalies.append({
                        "row_index": int(idx),
                        "value": float(val),
                        "lower_bound": round(float(lower_bound), 2),
                        "upper_bound": round(float(upper_bound), 2),
                    })

            if col_anomalies:
                anomalies_by_column[col] = {
                    "count": len(col_anomalies),
                    "anomalies": col_anomalies[:10], # Cap display sample
                }

        total_anomalous_rows = len(anomalous_row_indices)

        return {
            "status": "SUCCESS",
            "detection_method": method,
            "metrics_analyzed": target_cols,
            "total_records_analyzed": len(df),
            "anomalies_detected_count": total_anomalous_rows,
            "anomaly_rate_pct": round(total_anomalous_rows / len(df) * 100, 2),
            "anomalies_by_column": anomalies_by_column,
        }

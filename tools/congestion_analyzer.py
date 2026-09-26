"""Congestion Analyzer Tool for dynamic congestion metric evaluation."""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from .base_tool import BaseTool


class CongestionAnalyzerTool(BaseTool):
    """Analyzes traffic congestion indicators from available metrics."""

    def __init__(self):
        super().__init__(
            name="congestion_analyzer_tool",
            description="Evaluates speed, volume, occupancy, travel time, delay, and density indicators dynamically.",
            capability="congestion_analysis"
        )

    def execute(self, df: pd.DataFrame, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute dynamic congestion evaluation."""
        if not self.validate_input(df):
            return {
                "status": "INSUFFICIENT_DATA",
                "available_indicators": [],
                "congestion_level": "UNKNOWN",
            }

        cols = [c.lower() for c in df.columns]
        indicator_map = {}

        # Detect available indicator columns
        for col in df.columns:
            clow = col.lower()
            if any(k in clow for k in ["speed", "velocity"]):
                indicator_map["speed"] = col
            elif any(k in clow for k in ["vehicle_count", "volume", "flow", "count"]):
                indicator_map["vehicle_count"] = col
            elif any(k in clow for k in ["occupancy", "occ"]):
                indicator_map["occupancy"] = col
            elif any(k in clow for k in ["travel_time", "duration"]):
                indicator_map["travel_time"] = col
            elif any(k in clow for k in ["delay", "lag"]):
                indicator_map["delay"] = col
            elif any(k in clow for k in ["density"]):
                indicator_map["density"] = col

        available_indicators = list(indicator_map.keys())

        if not available_indicators:
            return {
                "status": "INSUFFICIENT_DATA",
                "message": "No standard congestion indicators (speed, count, occupancy, delay, density, travel_time) detected in dataset.",
                "available_indicators": [],
                "congestion_summary": {},
            }

        metrics_summary: Dict[str, Any] = {}
        congestion_scores: List[float] = []

        # Analyze Speed
        if "speed" in indicator_map:
            col = indicator_map["speed"]
            valid_speed = df[col].dropna()
            if not valid_speed.empty:
                avg_speed = float(valid_speed.mean())
                min_speed = float(valid_speed.min())
                metrics_summary["speed"] = {
                    "column": col,
                    "avg_speed": round(avg_speed, 2),
                    "min_speed": round(min_speed, 2),
                    "low_speed_observations": int((valid_speed < 25.0).sum()),
                }
                # Speed < 25 mph/kmh signals congestion
                if avg_speed < 20.0:
                    congestion_scores.append(0.9)
                elif avg_speed < 35.0:
                    congestion_scores.append(0.5)
                else:
                    congestion_scores.append(0.2)

        # Analyze Vehicle Count / Volume
        if "vehicle_count" in indicator_map:
            col = indicator_map["vehicle_count"]
            valid_vol = df[col].dropna()
            if not valid_vol.empty:
                avg_vol = float(valid_vol.mean())
                max_vol = float(valid_vol.max())
                metrics_summary["vehicle_count"] = {
                    "column": col,
                    "avg_vehicle_count": round(avg_vol, 2),
                    "max_vehicle_count": round(max_vol, 2),
                }

        # Analyze Occupancy
        if "occupancy" in indicator_map:
            col = indicator_map["occupancy"]
            valid_occ = df[col].dropna()
            if not valid_occ.empty:
                avg_occ = float(valid_occ.mean())
                # Normalize occupancy if scaled 0-100 or 0-1
                if avg_occ > 1.0:
                    avg_occ_pct = avg_occ / 100.0
                else:
                    avg_occ_pct = avg_occ
                metrics_summary["occupancy"] = {
                    "column": col,
                    "avg_occupancy_ratio": round(avg_occ_pct, 4),
                    "high_occupancy_observations": int((df[col] > (80.0 if avg_occ > 1.0 else 0.8)).sum()),
                }
                if avg_occ_pct > 0.75:
                    congestion_scores.append(0.85)
                elif avg_occ_pct > 0.45:
                    congestion_scores.append(0.5)
                else:
                    congestion_scores.append(0.15)

        # Analyze Delay
        if "delay" in indicator_map:
            col = indicator_map["delay"]
            valid_delay = df[col].dropna()
            if not valid_delay.empty:
                avg_delay = float(valid_delay.mean())
                metrics_summary["delay"] = {
                    "column": col,
                    "avg_delay": round(avg_delay, 2),
                    "max_delay": float(valid_delay.max()),
                }
                if avg_delay > 15.0:
                    congestion_scores.append(0.8)
                else:
                    congestion_scores.append(0.3)

        # Determine overall congestion classification
        overall_score = float(np.mean(congestion_scores)) if congestion_scores else 0.3
        if overall_score >= 0.7:
            overall_label = "HIGH_CONGESTION"
        elif overall_score >= 0.4:
            overall_label = "MODERATE_CONGESTION"
        else:
            overall_label = "LOW_CONGESTION"

        return {
            "status": "SUCCESS",
            "available_indicators": available_indicators,
            "overall_congestion_score": round(overall_score, 2),
            "overall_congestion_level": overall_label,
            "metrics_summary": metrics_summary,
        }

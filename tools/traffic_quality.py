"""Traffic Quality Tool for data hygiene and integrity auditing."""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from .base_tool import BaseTool


class TrafficQualityTool(BaseTool):
    """Assesses traffic data hygiene and integrity issues."""

    NON_NEGATIVE_FIELDS = ["vehicle_count", "volume", "speed", "occupancy", "travel_time", "delay", "density", "count"]

    def __init__(self):
        super().__init__(
            name="traffic_quality_tool",
            description="Audits dataset hygiene, missing ratios, invalid negative values, duplicate records, and timestamp formats.",
            capability="traffic_quality_analysis"
        )

    def execute(self, df: pd.DataFrame, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute quality audit without modifying underlying data."""
        if not self.validate_input(df):
            return {
                "status": "ERROR",
                "quality_score": 0.0,
                "issues_detected": ["Empty or invalid dataframe"],
            }

        total_rows = len(df)
        issues: List[Dict[str, Any]] = []

        # 1. Missing Values Check
        missing_counts = df.isnull().sum()
        high_missing_cols = missing_counts[missing_counts > 0.3 * total_rows].to_dict()
        if high_missing_cols:
            issues.append({
                "category": "HIGH_MISSING_DATA",
                "severity": "MEDIUM",
                "details": f"Columns with >30% missing values: {high_missing_cols}",
            })

        # 2. Duplicate Rows Check
        duplicate_count = int(df.duplicated().sum())
        if duplicate_count > 0:
            issues.append({
                "category": "DUPLICATE_RECORDS",
                "severity": "LOW" if duplicate_count < 0.05 * total_rows else "MEDIUM",
                "details": f"Found {duplicate_count} duplicate rows ({round(duplicate_count/total_rows*100, 2)}% of total)",
            })

        # 3. Negative Metric Values Check
        negative_issues = {}
        for col in df.select_dtypes(include=[np.number]).columns:
            clow = col.lower()
            if any(field in clow for field in self.NON_NEGATIVE_FIELDS):
                neg_count = int((df[col] < 0).sum())
                if neg_count > 0:
                    negative_issues[col] = neg_count

        if negative_issues:
            issues.append({
                "category": "INVALID_NEGATIVE_VALUES",
                "severity": "HIGH",
                "details": f"Impossible negative values detected in columns: {negative_issues}",
            })

        # 4. Timestamp Validation Check
        time_cols = [c for c in df.columns if any(t in c.lower() for t in ["timestamp", "time", "date"])]
        timestamp_issues = 0
        for tcol in time_cols:
            try:
                pd.to_datetime(df[tcol], errors="coerce")
                invalid_ts = df[tcol].dropna()[pd.to_datetime(df[tcol], errors="coerce").isna()]
                if not invalid_ts.empty:
                    timestamp_issues += len(invalid_ts)
            except Exception:
                timestamp_issues += len(df[tcol])

        if timestamp_issues > 0:
            issues.append({
                "category": "MALFORMED_TIMESTAMPS",
                "severity": "MEDIUM",
                "details": f"Detected {timestamp_issues} malformed datetime records across time columns: {time_cols}",
            })

        # Calculate Quality Score (0 - 100 scale)
        deductions = 0.0
        if duplicate_count > 0:
            deductions += min(20.0, (duplicate_count / total_rows) * 100)
        if negative_issues:
            deductions += 30.0
        if high_missing_cols:
            deductions += 25.0
        if timestamp_issues > 0:
            deductions += 15.0

        quality_score = max(0.0, round(100.0 - deductions, 2))

        return {
            "status": "SUCCESS",
            "quality_score": quality_score,
            "total_records_audited": total_rows,
            "total_issues_found": len(issues),
            "issues": issues,
            "is_data_usable": quality_score >= 40.0,
        }

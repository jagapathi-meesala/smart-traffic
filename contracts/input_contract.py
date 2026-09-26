"""Input contract for ingesting and validating generic traffic data."""

import os
import json
from typing import Dict, Any, Union, List, Tuple
import pandas as pd


class InputContract:
    """Validates raw traffic data inputs from various sources."""

    KNOWN_TRAFFIC_FIELDS = {
        "timestamp", "vehicle_count", "volume", "speed", "occupancy",
        "travel_time", "delay", "density", "incident", "incident_type",
        "incident_severity", "road_segment", "location", "lane_count"
    }

    @classmethod
    def validate_and_load(cls, input_data: Union[str, Dict[str, Any], List[Dict[str, Any]], pd.DataFrame]) -> Tuple[bool, str, pd.DataFrame, Dict[str, Any]]:
        """
        Validate input format and parse into a standard pandas DataFrame.
        Returns: (is_valid, message, dataframe, metadata)
        """
        metadata: Dict[str, Any] = {
            "source_type": "unknown",
            "detected_fields": [],
            "missing_standard_fields": [],
            "row_count": 0,
        }

        df: pd.DataFrame = pd.DataFrame()

        try:
            if isinstance(input_data, str):
                if not os.path.exists(input_data):
                    return False, f"File path does not exist: {input_data}", df, metadata
                
                ext = os.path.splitext(input_data)[1].lower()
                metadata["source_type"] = f"file_{ext.lstrip('.')}"
                
                if ext == ".csv":
                    df = pd.read_csv(input_data)
                elif ext == ".json":
                    with open(input_data, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if isinstance(data, list):
                        df = pd.DataFrame(data)
                    elif isinstance(data, dict):
                        if "records" in data and isinstance(data["records"], list):
                            df = pd.DataFrame(data["records"])
                        elif "data" in data and isinstance(data["data"], list):
                            df = pd.DataFrame(data["data"])
                        else:
                            df = pd.DataFrame([data])
                    else:
                        return False, "JSON content must be an array or dictionary of traffic records", df, metadata
                else:
                    return False, f"Unsupported file extension: {ext}. Expected .csv or .json", df, metadata

            elif isinstance(input_data, list):
                metadata["source_type"] = "in_memory_list"
                df = pd.DataFrame(input_data)

            elif isinstance(input_data, dict):
                metadata["source_type"] = "in_memory_dict"
                if "records" in input_data and isinstance(input_data["records"], list):
                    df = pd.DataFrame(input_data["records"])
                elif "data" in input_data and isinstance(input_data["data"], list):
                    df = pd.DataFrame(input_data["data"])
                else:
                    df = pd.DataFrame([input_data])

            elif isinstance(input_data, pd.DataFrame):
                metadata["source_type"] = "pandas_dataframe"
                df = input_data.copy()

            else:
                return False, f"Unsupported input type: {type(input_data)}", df, metadata

            if df.empty:
                return False, "Input traffic dataset is empty", df, metadata

            # Clean column names
            df.columns = [str(c).strip().lower() for c in df.columns]
            
            detected = list(df.columns)
            metadata["detected_fields"] = detected
            metadata["row_count"] = len(df)
            metadata["missing_standard_fields"] = list(cls.KNOWN_TRAFFIC_FIELDS - set(detected))

            return True, "Data successfully parsed and validated", df, metadata

        except Exception as e:
            return False, f"Error parsing traffic data input: {str(e)}", df, metadata

"""Synthetic demo traffic data generator for offline testing."""

import os
import argparse
import random
from datetime import datetime, timedelta
import pandas as pd


def generate_demo_traffic_data(num_rows: int = 100) -> pd.DataFrame:
    """
    Generate synthetic traffic observation dataset.
    Clearly labeled as generic synthetic data without real city names or real locations.
    """
    random.seed(42) # Deterministic generation for testing
    
    corridors = ["Corridor_Alpha", "Corridor_Beta", "Corridor_Gamma", "Corridor_Delta"]
    incidents = ["None", "Breakdown", "Minor_Debris", "Signal_Glitch", "None", "None"]
    severities = ["Low", "Medium", "High"]

    start_time = datetime(2026, 9, 26, 8, 0, 0)
    records = []

    for i in range(num_rows):
        ts = start_time + timedelta(minutes=5 * i)
        corridor = random.choice(corridors)
        
        # Simulate base speed & volume
        base_speed = random.uniform(25.0, 65.0)
        base_count = random.randint(30, 180)
        
        incident_type = random.choice(incidents)
        incident = "None" if incident_type == "None" else incident_type
        severity = random.choice(severities) if incident != "None" else "None"

        # If incident occurs, lower speed and increase occupancy/delay
        if incident != "None":
            speed = max(5.0, base_speed - random.uniform(15.0, 30.0))
            occupancy = min(0.98, random.uniform(0.70, 0.95))
            delay = random.uniform(10.0, 45.0)
        else:
            speed = base_speed
            occupancy = random.uniform(0.15, 0.60)
            delay = random.uniform(0.0, 8.0)

        records.append({
            "timestamp": ts.isoformat(),
            "road_segment": corridor,
            "vehicle_count": base_count,
            "speed": round(speed, 2),
            "occupancy": round(occupancy, 4),
            "travel_time": round(random.uniform(2.0, 15.0) + delay / 60.0, 2),
            "delay": round(delay, 2),
            "density": round(base_count / random.uniform(1.5, 3.0), 2),
            "incident": incident,
            "incident_severity": severity,
            "data_source": "synthetic_generator_v1",
        })

    return pd.DataFrame(records)


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic traffic observation data.")
    parser.add_argument("--output", type=str, default="demo_traffic.csv", help="Output path (.csv or .json)")
    parser.add_argument("--rows", type=int, default=100, help="Number of records to generate")
    args = parser.parse_args()

    df = generate_demo_traffic_data(args.rows)

    ext = os.path.splitext(args.output)[1].lower()
    if ext == ".json":
        df.to_json(args.output, orient="records", indent=2)
    else:
        df.to_csv(args.output, index=False)

    print(f"✅ Generated {len(df)} synthetic traffic observation records -> {args.output}")


if __name__ == "__main__":
    main()

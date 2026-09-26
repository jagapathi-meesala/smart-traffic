"""CLI script for running smart-traffic-management-agent on input data."""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.agent_core import AgentCore


def main():
    parser = argparse.ArgumentParser(description="Run Smart Traffic Management Agent on traffic dataset.")
    parser.add_argument("--input", type=str, required=True, help="Path to input traffic file (.csv or .json)")
    parser.add_argument("--output", type=str, default=None, help="Optional output JSON path to save analytical report")
    parser.add_argument("--zscore", type=float, default=2.5, help="Z-score anomaly threshold (default 2.5)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    print(f"🚦 Running Smart Traffic Management Agent on: {args.input}")
    
    agent = AgentCore()
    options = {"zscore_threshold": args.zscore}
    
    report = agent.run_analysis(args.input, options=options)

    if report.get("status") == "FAILED":
        print(f"❌ Execution Failed: {report.get('error')}", file=sys.stderr)
        sys.exit(1)

    # Print JSON output to stdout or file
    report_json = json.dumps(report, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report_json)
        print(f"✅ Analytical report successfully saved to: {args.output}")
    else:
        print("\n" + report_json)

    sys.exit(0)


if __name__ == "__main__":
    main()

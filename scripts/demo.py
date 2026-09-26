"""Interactive offline demonstration script for smart-traffic-management-agent."""

import json
import os
import sys

# Add project root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.generate_demo_data import generate_demo_traffic_data
from core.agent_core import AgentCore
from verification.passport_trust_verifier import PassportTrustVerifier


def main():
    print("================================================================================")
    print(" 🚦 SMART TRAFFIC MANAGEMENT AGENT — DEMO EXECUTION")
    print("================================================================================")

    # 1. Generate Synthetic Data
    print("\n[1/5] Generating synthetic traffic dataset...")
    df = generate_demo_traffic_data(num_rows=60)
    print(f"      Created {len(df)} synthetic records across corridors.")

    # 2. Initialize Core & Load Passport
    print("\n[2/5] Initializing AgentCore & Loading Passport Manifest...")
    core = AgentCore()
    summary = core.passport_manager.get_summary()
    print(f"      Agent Name : {summary['name']}")
    print(f"      Agent ID   : {summary['agent_id']}")
    print(f"      Version    : {summary['version']}")
    print(f"      Spec Ver   : {summary['spec_version']}")

    # 3. Discover Tools
    print("\n[3/5] Discovering Registered Capabilities & Tools...")
    tools = core.registry.list_tools()
    for t in tools:
        print(f"      • Tool: {t['name']:<35} | Capability: {t['capability']}")

    # 4. Execute Analysis Pipeline
    print("\n[4/5] Running Analytical Pipeline...")
    report = core.run_analysis(df)

    print("\n" + "="*80)
    print(" 📊 ANALYSIS REPORT SUMMARY")
    print("="*80)
    print(f" Data Quality Score  : {report['data_quality']['quality_score']}/100")
    print(f" Congestion Level    : {report['congestion_analysis']['level']} (Score: {report['congestion_analysis']['score']})")
    print(f" Active Incidents    : {report['incident_analysis']['total_incidents']}")
    print(f" Anomalies Detected  : {report['anomaly_detection']['anomalies_count']}")

    print("\n 💡 EVIDENCE-BASED RECOMMENDATIONS:")
    for idx, rec in enumerate(report["recommendations"], 1):
        print(f"   {idx}. [{rec['category'].upper()}] {rec['action']}")
        print(f"      Reason: {rec['reason']}")
        print(f"      Confidence: {rec['confidence_strength']}")
        print(f"      Limitations: {rec['limitations']}\n")

    # 5. Passport Trust Verification
    print("[5/5] Verifying Passport Trust & Integrity...")
    verifier = PassportTrustVerifier()
    trust_result = verifier.verify_trust()
    print(f"      Passport Trust Status: {trust_result['status']}")
    print("================================================================================")
    print(" ✅ DEMO EXECUTION COMPLETE (Offline, Deterministic)")
    print("================================================================================")


if __name__ == "__main__":
    main()

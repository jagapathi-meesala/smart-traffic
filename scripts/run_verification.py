"""CLI script running full Agent Passport and HiDevs verification suite."""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from verification import (
    PassportTrustVerifier,
    PortabilityVerifier,
    FrameworkVerifier,
    SecurityAudit,
    HardcodingAudit,
    HiDevsReadinessVerifier,
)


def main():
    print("================================================================================")
    print(" 🛡️ SMART TRAFFIC MANAGEMENT AGENT — FULL VERIFICATION SUITE")
    print("================================================================================")

    # 1. Trust Verification
    print("\n[1/6] Running Passport Trust Verifier...")
    trust_res = PassportTrustVerifier().verify_trust()
    print(f"      Status: {trust_res['status']} | Verified Tools: {trust_res['verified_tools_count']}")

    # 2. Portability Verification
    print("\n[2/6] Running Portability Verifier...")
    port_res = PortabilityVerifier().verify_portability()
    print(f"      Status: {port_res['status']} | Framework Independent: {port_res['framework_independent']}")

    # 3. Framework Verification
    print("\n[3/6] Running Framework Neutrality Verifier...")
    fw_res = FrameworkVerifier().verify_framework()
    print(f"      Status: {fw_res['status']} | Descriptor: {fw_res['framework_status_descriptor']}")

    # 4. Security Audit
    print("\n[4/6] Running Security Audit...")
    sec_res = SecurityAudit().run_audit()
    print(f"      Status: {sec_res['status']} | Scanned Files: {sec_res['scanned_files_count']} | Findings: {sec_res['findings_count']}")

    # 5. Hardcoding Audit
    print("\n[5/6] Running Hardcoding Audit...")
    hc_res = HardcodingAudit().run_audit()
    print(f"      Status: {hc_res['status']} | Issues Count: {hc_res['issues_count']}")

    # 6. HiDevs Readiness Verification
    print("\n[6/6] Running HiDevs Readiness Verifier...")
    hidevs_res = HiDevsReadinessVerifier().verify_readiness()
    print(f"      Status: {hidevs_res['readiness_status']} | All Checks Passed: {hidevs_res['all_checks_passed']}")

    summary = {
        "passport_trust": trust_res["status"],
        "portability": port_res["status"],
        "framework": fw_res["status"],
        "security": sec_res["status"],
        "hardcoding": hc_res["status"],
        "hidevs_readiness": hidevs_res["readiness_status"],
    }

    print("\n" + "="*80)
    print(" 📋 VERIFICATION SUMMARY MATRIX")
    print("="*80)
    for k, v in summary.items():
        print(f"  • {k:<25}: {v}")
    print("================================================================================")

    all_passed = (
        trust_res["status"] == "PASSED" and
        port_res["status"] == "PASSED" and
        fw_res["status"] == "PASSED" and
        sec_res["status"] == "PASSED" and
        hc_res["status"] == "PASSED" and
        hidevs_res["readiness_status"] == "READY"
    )

    if all_passed:
        print(" 🎉 ALL VERIFICATION SUITES PASSED (HiDevs Submission Ready)")
        sys.exit(0)
    else:
        print(" ❌ SOME VERIFICATION SUITES FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()

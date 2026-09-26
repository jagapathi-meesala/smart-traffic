# EXPLAINABILITY.md - Smart Traffic Management Agent Explainability Architecture

## Purpose
The Smart Traffic Management Agent is an autonomous, framework-independent analytical agent built for the HiDevs x Lyzr Agent Passport challenge. It provides offline, deterministic traffic data profiling, congestion scoring, data hygiene auditing, anomaly detection, incident analysis, and evidence-based recommendation generation.

## Inputs and Data Sources
The agent accepts generic structured traffic observation data in formats such as CSV, JSON, or in-memory Python dictionaries and lists. It dynamically discovers available traffic fields—such as speed, vehicle count, occupancy, travel time, delay, density, timestamp, road segment, and incident records—without enforcing rigid predefined schemas.

## Decision and Reasoning
All analytical decisions, congestion classifications, and recommendations are derived deterministically from empirical evidence using explicit mathematical models such as Z-score anomaly bounds, IQR statistical thresholds, and multi-indicator congestion formulas. Recommendations explicitly link each proposed action to specific supporting metrics, confidence levels, and data limitations to ensure full auditability.

## Tools and Capabilities
The system exposes seven independent domain tools: `traffic_data_profiler_tool`, `congestion_analyzer_tool`, `traffic_quality_tool`, `incident_analysis_tool`, `traffic_anomaly_detector_tool`, `traffic_management_recommender_tool`, and `traffic_report_tool`. Each tool corresponds to a distinct passport capability (`traffic_data_profiling`, `congestion_analysis`, `traffic_quality_analysis`, `incident_analysis`, `traffic_anomaly_detection`, `traffic_management_recommendation`, and `traffic_analytical_reporting`) and operates via strict input/output contracts.

## Limitations and Constraints
The agent functions exclusively as an offline analytical decision-support system and does not directly connect to or control physical traffic light hardware or live municipal infrastructure. If certain expected fields (such as incident classifications or temporal timestamps) are missing from input data, affected tools return explicit fallback states (`INSUFFICIENT_DATA` or `UNAVAILABLE`) rather than manufacturing false findings.

## Portability
The core architecture decouples business logic into an framework-agnostic `AgentCore` module that communicates strictly through abstract passport adapters. This allows the agent to run seamlessly as a standalone Python CLI tool, within pytest execution environments, or wrapped inside external agent frameworks without modifying internal domain tools.

## Verification
System integrity and compliance are verified dynamically through an automated verification suite containing six specialized auditors: Passport Trust, Portability, Framework Neutrality, Security Audit, Hardcoding Audit, and HiDevs Readiness. These verifiers dynamically inspect passport manifests, validate execution behavior, scan for credential leaks, check hardcoding rules, and ensure offline test execution.

## Failure Handling
Input processing and execution follow a stateful `BehaviorContract` lifecycle spanning input validation, passport loading, capability matching, tool discovery, execution, result validation, and response generation. Structured exceptions and error states ensure that corrupt files, missing fields, or unavailable LLM providers trigger graceful fallback responses rather than abrupt system crashes.

## Expected Output
The final output produced by the agent is a structured Python dictionary or JSON document containing a comprehensive analytical report. This report incorporates dataset summaries, data quality health scores, congestion indicator findings, incident impact summaries, detected anomalies, evidence-backed recommendations, and system verification metadata.

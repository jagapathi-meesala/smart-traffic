# Smart Traffic Management Agent

[![Agent Passport Standard](https://img.shields.io/badge/Agent%20Passport-v0.1.0-blue.svg)](agent.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![HiDevs Ready](https://img.shields.io/badge/HiDevs%20Ready-Verified-green.svg)](scripts/run_verification.py)

An autonomous, framework-independent, portable analytical AI agent built for the **HiDevs x Lyzr Agent Passport** challenge. The agent ingests generic traffic observation datasets (CSV, JSON, Python dictionaries), assesses data hygiene, evaluates congestion indicators, detects statistical anomalies, analyzes incident impacts, and generates transparent, evidence-based traffic management recommendations completely offline.

> **IMPORTANT DISCLAIMER**: This system is strictly an **analytical and decision-support recommendation agent**. It does **NOT** directly connect to, signal to, or control real-world physical traffic lights, emergency dispatch networks, or municipal infrastructure.

---

## 🏛️ Architecture

The architecture guarantees strict framework independence, provider neutrality, and offline-first execution. `AgentCore` serves as the single source of truth for business logic.

```
External Framework (Lyzr / Custom)
        ↓
Framework Adapter (`adapters/framework_adapter.py`)
        ↓
Portable Adapter (`adapters/portable_adapter.py`)
        ↓
AgentCore (`core/agent_core.py`)
        ↓
Execution Engine (`core/execution_engine.py`)
        ↓
PassportManager  |  ToolRegistry  |  BehaviorContract
        ↓
Traffic Domain Tools (`tools/*`)
```

---

## 🎯 Purpose & Scope

- **Offline-First Deterministic Analysis**: Analyzes traffic datasets locally using pure statistical formulas (Z-Score, IQR) without requiring internet connectivity or paid API keys.
- **Schema-Agnostic Ingestion**: Ingests generic CSV, JSON, and list/dict data structures. Automatically detects available fields such as `speed`, `vehicle_count`, `occupancy`, `travel_time`, `delay`, `density`, `timestamp`, and `incident`.
- **Transparent Evidence-Based Recommendations**: Links every recommendation directly to observed metrics, confidence bounds, and data limitations.
- **Passport Compliance**: Fully compliant with the `spec_version: "0.1.0"` Agent Passport standard.

---

## 🛠️ Capabilities & Tools

| Capability | Tool Name | Description |
|---|---|---|
| `traffic_data_profiling` | `traffic_data_profiler_tool` | Profiles dataset size, column types, missing values, duplicates, and numerical distributions. |
| `congestion_analysis` | `congestion_analyzer_tool` | Evaluates speed drops, volume spikes, travel delays, and density metrics. |
| `traffic_quality_analysis` | `traffic_quality_tool` | Audits data hygiene, invalid bounds, malformed timestamps, and suspicious records. |
| `incident_analysis` | `incident_analysis_tool` | Categorizes incidents by severity, type, and temporal impact (with graceful fallback). |
| `traffic_anomaly_detection` | `traffic_anomaly_detector_tool` | Detects statistical outliers using Z-score, IQR, or rolling metrics. |
| `traffic_management_recommendation` | `traffic_management_recommender_tool` | Generates transparent, evidence-backed traffic mitigation strategies. |
| `traffic_analytical_reporting` | `traffic_report_tool` | Synthesizes all findings into a unified structured analytical report. |

---

## 🚀 Ingestion & Input Formats

The agent accepts generic tabular traffic data. No single field is mandatory; missing fields trigger structured fallbacks (`INSUFFICIENT_DATA` / `UNAVAILABLE`).

### Supported Formats
- **CSV files** (`.csv`)
- **JSON files** (`.json`)
- **In-Memory Python Objects** (list of dicts or DataFrame)

### Example Input CSV (`traffic_sample.csv`)
```csv
timestamp,road_segment,vehicle_count,speed,occupancy,incident
2026-09-26T08:00:00,Corridor_A,145,22.5,0.85,Breakdown
2026-09-26T08:05:00,Corridor_A,150,18.0,0.92,Breakdown
2026-09-26T08:10:00,Corridor_B,45,65.0,0.20,None
```

---

## 💻 Installation & Usage

### 1. Clone & Setup Environment
```bash
git clone https://github.com/hidevs/smart-traffic-management-agent.git
cd smart-traffic-management-agent

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate Synthetic Demo Data
```bash
python scripts/generate_demo_data.py --output demo_traffic.csv --rows 100
```

### 3. Run Analysis via CLI
```bash
# Analyze CSV file
python scripts/run_agent.py --input demo_traffic.csv

# Analyze JSON file
python scripts/run_agent.py --input demo_traffic.json
```

### 4. Run Offline Interactive Demo Script
```bash
python scripts/demo.py
```

---

## 🧪 Testing & Verification

Run the comprehensive unit test suite:
```bash
pytest tests/ -v
```

Run the full Agent Passport verification suite:
```bash
python scripts/run_verification.py
```

The verification suite evaluates:
1. **Passport Trust**: Manifest schema validity, capability matching, and tool registry integrity.
2. **Portability**: Direct `AgentCore` execution vs adapter execution.
3. **Framework Neutrality**: Structural adapter validation and SDK detection.
4. **Security Audit**: Codebase scanning for API credentials and secret leaks.
5. **Hardcoding Audit**: Checking for hardcoded secrets, fake external calls, or static assumptions.
6. **HiDevs Readiness**: Manifest specs, metadata files (`SOUL.md`, `DUTIES.md`, `EXPLAINABILITY.md`), and test results.

---

## ⚙️ Provider Configuration (Optional)

The agent operates 100% offline by default. If optional OpenAI / LLM integration is desired:
1. Copy `.env.example` to `.env`.
2. Populate `OPENAI_API_KEY`.
3. If credentials or SDKs are omitted, the provider boundary safely returns `SKIPPED — PROVIDER_NOT_CONFIGURED` without failing.

---

## 🔒 Security & Privacy

- No real credentials, API tokens, or keys are checked into source code.
- Sensitive environment variables are masked and never printed in logs.
- Strict input validation prevents script injections or malicious data execution.

---

## 📄 License & Passport Standard

Distributed under the MIT License. Complies with the **Agent Passport Specification v0.1.0**.

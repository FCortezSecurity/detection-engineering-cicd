# Detection Engineering CI/CD Platform

An automated detection validation pipeline that simulates real MITRE ATT&CK techniques, validates custom Wazuh detection rules, and generates professional SOC coverage reports.

## Architecture
## Features

- Automated ATT&CK technique simulation via Atomic Red Team
- Custom Wazuh detection rules mapped to MITRE ATT&CK
- CI/CD validation pipeline with pass/fail coverage scoring
- HTML ATT&CK coverage dashboard
- AI-generated SOC incident reports via Claude API
- 100% detection coverage across 5 ATT&CK techniques

## Coverage

| Technique | Name | Tactic | Rule | Status |
|-----------|------|--------|------|--------|
| T1057 | Process Discovery | Discovery | 100002 | ✅ PASS |
| T1059.001 | PowerShell Execution | Execution | 100004 | ✅ PASS |
| T1082 | System Info Discovery | Discovery | 100006 | ✅ PASS |
| T1053.005 | Scheduled Task | Persistence | 100003 | ✅ PASS |
| T1027 | Base64 Defense Evasion | Defense Evasion | 100007 | ✅ PASS |

## Stack

- **SIEM:** Wazuh 4.7.5 (Docker)
- **Telemetry:** Sysmon (SwiftOnSecurity config)
- **Simulation:** Atomic Red Team
- **Target:** Windows 11
- **Pipeline:** Python 3
- **AI:** Claude API (Anthropic)

## Usage

```bash
# Set your API key
export ANTHROPIC_API_KEY=your-key-here

# Run full pipeline
bash pipeline/run_pipeline.sh

# Run individual components
python3 pipeline/validate_detections.py
python3 pipeline/generate_dashboard.py
python3 pipeline/generate_report.py
```

## Project Structure
detection-engineering-cicd/
├── pipeline/
│   ├── validate_detections.py   # CI/CD validation engine
│   ├── generate_dashboard.py    # HTML coverage dashboard
│   ├── generate_report.py       # AI incident report
│   └── run_pipeline.sh          # Master runner
├── detection-rules/
│   └── local_rules.xml          # Custom Wazuh detection rules
├── reports/                     # Generated coverage reports
└── docs/                        # Documentation
## Results

![Coverage](https://img.shields.io/badge/ATT%26CK%20Coverage-100%25-brightgreen)
![Techniques](https://img.shields.io/badge/Techniques-5%2F5-brightgreen)
![SIEM](https://img.shields.io/badge/SIEM-Wazuh-blue)

- **5/5 techniques detected**
- **100% ATT&CK coverage**
- **Automated end-to-end in one command**

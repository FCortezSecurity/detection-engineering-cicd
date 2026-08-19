# Detection Engineering CI/CD Platform

An automated detection validation pipeline that simulates real MITRE ATT&CK techniques against a live Windows 11 endpoint and Kubernetes cluster, validates custom Wazuh detection rules, and generates professional SOC coverage reports — end to end in a single command.

![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen) ![Techniques](https://img.shields.io/badge/Techniques-11-blue) ![SIEM](https://img.shields.io/badge/SIEM-Wazuh-orange) ![Platform](https://img.shields.io/badge/Platform-Windows%2011%20%2B%20K8s-lightgrey) ![AI](https://img.shields.io/badge/AI-Claude%20API-purple)

## Pipeline — 100% ATT&CK Coverage
![Pipeline](src/06-html-dashboard.png)

## Overview

Most detection engineering work happens in silos — someone writes a rule, deploys it, and hopes it works. This project solves that by building a CI/CD pipeline for detections: every rule is automatically tested against a real attack simulation and must pass before it's considered valid coverage.

This mirrors how mature security teams at enterprise organizations validate their detection content — the difference is this was built from scratch as a solo project, and now spans both Windows endpoint telemetry and Kubernetes audit logs.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     ATTACK SIMULATION LAYER                     │
│   Atomic Red Team (Windows) │ Manual K8s Attack Simulation      │
└─────────────────────────┬───────────────────────────────────────┘
                          │ Sysmon Telemetry / K8s Audit Logs
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DETECTION LAYER                          │
│  Sysmon/K8s Audit → Wazuh Agent → Wazuh Manager → Custom Rules  │
└─────────────────────────┬───────────────────────────────────────┘
                          │ Alerts + Rule Firing
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                       VALIDATION LAYER                          │
│   Python Pipeline → Wazuh Indexer API → PASS/FAIL per Technique│
└─────────────────────────┬───────────────────────────────────────┘
                          │ Coverage Data
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                       REPORTING LAYER                           │
│        HTML Dashboard + Claude AI SOC Incident Report          │
└─────────────────────────────────────────────────────────────────┘
```

## ATT&CK Coverage Results

### Windows Endpoint Detections

| Technique | Name | Tactic | Custom Rule | Status |
|---|---|---|---|---|
| T1057 | Process Discovery | Discovery | 100002 | ✅ PASS |
| T1059.001 | PowerShell Execution | Execution | 100004 | ✅ PASS |
| T1082 | System Information Discovery | Discovery | 100006 | ✅ PASS |
| T1053.005 | Scheduled Task Persistence | Persistence | 100003 | ✅ PASS |
| T1027 | Base64 Defense Evasion | Defense Evasion | 100007 | ✅ PASS |

**5/5 techniques detected — 100% coverage**

### Kubernetes Attack Path Detections

Extended the platform to ingest Kubernetes API audit logs and detect attack paths against the cluster control plane, alongside the existing Windows endpoint coverage.

| Rule ID | Description | MITRE Technique | Severity |
|---|---|---|---|
| 100100 | Base Kubernetes API audit event (parent rule) | — | Informational |
| 100101 | Privileged container created — possible node escape | T1611 (Escape to Host) | Critical |
| 100102 | Pod created with hostPath volume mount — possible container escape | T1611 (Escape to Host) | High |
| 100103 | New ClusterRoleBinding grants cluster-admin — critical privilege escalation | T1078.002 (Valid Accounts) | Critical |
| 100104 | ServiceAccount read a Secret outside kube-system — possible credential exposure | T1552.007 (Unsecured Credentials: Container API) | Medium |
| 100105 | Repeated privileged pod creation — possible automated exploitation | T1611 (Escape to Host) | Critical |

Rule 100105 uses `if_matched_sid` correlation against rule 100101 with a frequency/timeframe threshold, flagging automated or scripted exploitation attempts rather than one-off privileged pod creation.

## Features

- Automated attack simulation via Atomic Red Team on a live Windows 11 endpoint
- Kubernetes API audit log ingestion for cluster-level attack path detection
- Deep telemetry via Sysmon with SwiftOnSecurity configuration
- Custom detection rules authored in Wazuh XML, mapped to MITRE ATT&CK
- CI/CD validation pipeline that queries the Wazuh indexer API and scores each rule PASS/FAIL
- HTML coverage dashboard with ATT&CK technique breakdown and coverage ring
- AI-generated SOC incident report via Claude API — professional markdown output
- Single command execution — entire pipeline runs with `bash pipeline/run_pipeline.sh`

## Screenshots

### Lab Environment — Wazuh Agent Active
![Wazuh Agent](src/01-wazuh-agent-active.png)

Windows 11 host connected to Wazuh manager with active status — the foundation of the detection lab.

### Attack Simulation — Sysmon Telemetry Flooding In
![Sysmon Events](src/02-sysmon-events-firing.png)

223+ Sysmon events captured during ATT&CK technique simulation — discovery activity, net.exe account enumeration, and abnormal process chains all visible.

### Attack Simulation — High Severity Detections
![Attack Detections](src/03-sysmon-attack-detections.png)

Level 15 (critical) alerts firing — executable dropped in malware-common folder and Base64-like pattern detected in registry key (T1027 Defense Evasion).

### Custom Detection Rules Firing
![Custom Rules](src/04-custom-rules-firing.png)

Custom rule IDs 100004 and 100006 firing — these are not built-in Wazuh rules. These were written specifically for this project, mapped to MITRE ATT&CK T1059.001 and T1082.

### ATT&CK Coverage Dashboard
![Dashboard](src/06-html-dashboard.png)

Auto-generated HTML dashboard showing 100% coverage ring, 5/5 techniques passed, with full ATT&CK technique breakdown.

## Stack

| Component | Technology |
|---|---|
| SIEM | Wazuh 4.7.5 (Docker) |
| Endpoint Telemetry | Sysmon + SwiftOnSecurity config |
| Cluster Telemetry | Kubernetes API audit logs |
| Attack Simulation | Atomic Red Team (invoke-atomicredteam) |
| Target Endpoint | Windows 11 |
| Detection Rules | Custom Wazuh XML rules |
| Pipeline | Python 3 |
| AI Reporting | Claude API (Anthropic) |
| Version Control | Git + GitHub |

## Project Structure

```
detection-engineering-cicd/
├── pipeline/
│   ├── validate_detections.py   # Core CI/CD validation engine
│   ├── generate_dashboard.py    # HTML ATT&CK coverage dashboard
│   ├── generate_report.py       # AI-powered SOC incident report
│   └── run_pipeline.sh          # Master pipeline runner
├── detection-rules/
│   └── local_rules.xml          # Custom Wazuh detection rules (Windows + K8s)
├── reports/                     # Generated coverage reports (JSON/HTML/MD)
├── src/                          # Project screenshots
└── attack-simulations/          # ATT&CK technique documentation
```

## Usage

```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY=your-key-here

# Run the full pipeline (validate + dashboard + AI report)
bash pipeline/run_pipeline.sh

# Or run individual components
python3 pipeline/validate_detections.py   # Validate all detection rules
python3 pipeline/generate_dashboard.py    # Generate HTML dashboard
python3 pipeline/generate_report.py       # Generate AI incident report
```

## Pipeline Output

```
============================================================
  Detection Engineering CI/CD Pipeline
  Full Run
============================================================

[1/3] Running detection validation...
[+] Wazuh API authenticated successfully

[*] Testing T1059.001 - PowerShell Execution
    [✓] PASS - Rule 100004 confirmed in alerts!

[*] Testing T1082 - System Information Discovery
    [✓] PASS - Rule 100006 confirmed in alerts!

[*] Testing T1057 - Process Discovery
    [✓] PASS - Rule 100002 confirmed in alerts!

[*] Testing T1053.005 - Scheduled Task Persistence
    [✓] PASS - Rule 100003 confirmed in alerts!

[*] Testing T1027 - Base64 Defense Evasion
    [✓] PASS - Rule 100007 confirmed in alerts!

============================================================
  DETECTION COVERAGE REPORT
  Total: 5 | Passed: 5 | Failed: 0 | Coverage: 100.0%
============================================================

[2/3] Generating coverage dashboard...
[+] Dashboard saved to reports/dashboard.html

[3/3] Generating AI incident report...
[+] AI incident report saved to reports/incident_report.md
============================================================
  Pipeline complete!
  Check reports/ folder for all outputs
============================================================
```

## Challenges & Problem Solving

This section documents the real technical obstacles encountered during this build and how they were resolved. Detection engineering is mostly debugging — this is what that actually looks like.

### Challenge 1: Wazuh Not Supported on Arch Linux

**Problem:** Wazuh's official install script (`wazuh-install.sh -a`) immediately exited with:
```
ERROR: Couldn't find type of system
```
Arch Linux is not in Wazuh's supported distro list and the script has no fallback.

**Solution:** Deployed Wazuh entirely via Docker using the official `wazuh-docker` single-node compose stack. This actually produced a more portable and reproducible environment than a native install would have.

**Lesson:** When a tool doesn't support your OS, containerization is often a cleaner solution than fighting the installer. The Docker deployment is also more realistic — most enterprise Wazuh deployments run containerized.

### Challenge 2: Disk Space Exhaustion Mid-Project

**Problem:** During PowerShell installation, the root partition hit 100% capacity:
```
Your Root partition is running out of disk space; 0 MiB remaining (0%)
df -h showed: /dev/sda2  49G  47G  0  100% /
```
Docker image layers from multiple previous security projects had consumed nearly all available space.

**Solution:** Ran `docker system prune -a --volumes -f` which safely removed unused images and volumes, recovering 4.7GB. Also cleared pacman cache and journal logs to recover additional space, bringing usage down to 80%.

**Lesson:** Docker image sprawl is a real operational concern in lab environments. Regular pruning and disk monitoring should be part of any lab hygiene practice.

### Challenge 3: Custom Detection Rules Not Firing (0% → 100%)

**Problem:** After writing 6 custom Wazuh rules using `if_sid` to chain from parent rules (92027, 92031, 92034), the validation pipeline showed 0% coverage — none of the custom rules were appearing in alerts even though parent rules were firing correctly with hundreds of hits.

**Diagnosis process:**
1. Confirmed parent rules were firing — hundreds of hits visible in dashboard
2. Confirmed rule XML syntax was valid — no parse errors on restart
3. Queried raw alerts log to see actual field values in Sysmon events
4. Discovered `tasklist.exe` and `wmic.exe` events were triggering different base Sysmon event IDs than expected
5. Found that `if_sid` on a rule that is itself already a child rule (like 92041) requires `if_matched_sid` instead

**Solution:**
- Changed base `if_sid` references to 61603 (raw Sysmon process creation event) for process-based rules
- Changed `if_sid` to `if_matched_sid` for the T1027 Base64 registry rule that chains from 92041
- Coverage went from 0% → 80% → 100% through iterative fixes

**Lesson:** Understanding the difference between `if_sid` and `if_matched_sid` in Wazuh's rule chaining model is critical knowledge for detection engineers writing custom rules. This same distinction resurfaced later in the Kubernetes rules — rule 100105 uses `if_matched_sid` to correlate repeated privileged pod creation against rule 100101, rather than re-matching the raw audit event.

### Challenge 4: Wazuh API Endpoint Mismatch

**Problem:** The initial pipeline used `/siem/alerts` endpoint to query for fired rules. All 5 techniques returned FAIL despite rules clearly visible firing in the Wazuh dashboard. The endpoint returned 404.

**Solution:** Switched to querying the Wazuh OpenSearch indexer directly at:
```
https://localhost:9200/wazuh-alerts-*/_search
```
Using OpenSearch DSL query format with bool/must filters for rule ID, agent ID, and timestamp range. This gave direct, accurate access to the alerts index.

**Lesson:** Always verify API endpoints against the specific version being run. The Wazuh API and the underlying OpenSearch indexer API are separate interfaces — the indexer query gives more flexibility and reliability for custom tooling.

### Challenge 5: API Key Exposed in Git Commit

**Problem:** GitHub's push protection blocked the push with:
```
remote: - GITHUB PUSH PROTECTION
remote: Push cannot contain secrets
remote: — Anthropic API Key —
remote: locations: commit: fa580416 path: pipeline/generate_report.py:15
```
The Anthropic API key had been hardcoded directly in the source file and was detected in commit history.

**Solution:**
- Replaced hardcoded key with `os.environ.get("ANTHROPIC_API_KEY")`
- Created `.env` file for local key storage and added to `.gitignore`
- Used `git filter-branch` to rewrite history and scrub the secret from all commits
- Force pushed the clean history

**Lesson:** Never hardcode secrets in source files — use environment variables from the start. GitHub's secret scanning is a valuable last line of defense but the correct practice is never committing secrets in the first place. This is standard practice in any production security environment.

## Key Takeaways for Interviews

**"What was the hardest part of this project?"**

The rule chaining issue — debugging why custom rules weren't firing despite parent rules working correctly required understanding Wazuh's internal rule evaluation model at a deep level. The fix was a single XML attribute change (`if_sid` → `if_matched_sid`) but finding it required systematic log analysis, reading raw alert output, and understanding how Wazuh chains multi-level rules. That kind of low-level debugging is what separates someone who uses security tools from someone who understands them.

**"How does this relate to real-world detection engineering?"**

Real detection engineering teams face the same core problem: rules get written and deployed but nobody validates they actually work against the techniques they're supposed to detect. Rules break silently when attacker behavior evolves. This pipeline automates that validation continuously — the same concept used by mature security teams running detection-as-code workflows. Extending it to Kubernetes audit logs also reflects a real shift in the industry: attack surface increasingly includes the orchestration layer, not just the endpoint.

**"Why did you choose this stack?"**

Wazuh because it's open source and widely deployed in enterprise environments. Sysmon because it's the gold standard for Windows endpoint telemetry. Atomic Red Team because it provides standardized, reproducible ATT&CK technique simulations used by real red teams. Kubernetes API audit logs because they're the ground-truth source for control-plane activity, and correlating them through the same Wazuh pipeline avoids maintaining a second, disconnected detection stack. The combination mirrors what actual blue teams use — this isn't a toy lab, it's a realistic enterprise simulation.

## Future Improvements

- [ ] Add GitHub Actions workflow to run pipeline automatically on every rule change
- [ ] Expand to 20+ ATT&CK techniques across more tactics
- [ ] Add Sigma rule conversion for multi-SIEM support (Splunk SPL, KQL)
- [ ] Integrate Splunk as second SIEM validation target
- [ ] Add detection drift alerting — notify when a previously passing rule starts failing
- [ ] Build ATT&CK Navigator heatmap JSON export
- [ ] Add cleanup/rollback for Atomic Red Team test artifacts
- [ ] Automate Kubernetes attack simulation (currently manual) to match the Atomic Red Team workflow used for Windows

## Author

Fernando Cortez Jr. — Security Engineer focused on detection engineering, cloud security, DFIR, and AI-assisted security operations.

GitHub: [@FCortezSecurity](https://github.com/FCortezSecurity)

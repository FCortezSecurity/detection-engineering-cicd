#!/usr/bin/env python3
"""
Detection Engineering CI/CD Pipeline
Validates Wazuh detection rules against MITRE ATT&CK simulations
"""

import requests
import json
import time
import urllib3
from datetime import datetime, timezone
from typing import Optional
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
WAZUH_HOST = "https://localhost:55000"
WAZUH_USER = "wazuh-wui"
WAZUH_PASS = "MyS3cr37P450r.*-"
AGENT_ID = "002"

# ATT&CK techniques to validate
TECHNIQUES = [
    {
        "id": "T1059.001",
        "name": "PowerShell Execution",
        "tactic": "Execution",
        "custom_rule_id": "100004",
        "expected_level": 12
    },
    {
        "id": "T1082",
        "name": "System Information Discovery",
        "tactic": "Discovery",
        "custom_rule_id": "100006",
        "expected_level": 8
    },
    {
        "id": "T1057",
        "name": "Process Discovery",
        "tactic": "Discovery",
        "custom_rule_id": "100002",
        "expected_level": 10
    },
    {
        "id": "T1053.005",
        "name": "Scheduled Task Persistence",
        "tactic": "Persistence",
        "custom_rule_id": "100003",
        "expected_level": 12
    },
    {
        "id": "T1027",
        "name": "Base64 Defense Evasion",
        "tactic": "Defense Evasion",
        "custom_rule_id": "100007",
        "expected_level": 14
    }
]

def get_wazuh_token() -> Optional[str]:
    """Authenticate to Wazuh API and get JWT token"""
    try:
        response = requests.post(
            f"{WAZUH_HOST}/security/user/authenticate",
            auth=(WAZUH_USER, WAZUH_PASS),
            verify=False,
            timeout=10
        )
        if response.status_code == 200:
            token = response.json()["data"]["token"]
            print("[+] Wazuh API authenticated successfully")
            return token
        else:
            print(f"[-] Auth failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"[-] Connection error: {e}")
        return None

def check_rule_fired(token: str, rule_id: str) -> bool:
    """Check Wazuh alerts index for a specific rule ID"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    # Use Wazuh indexer API to search alerts
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"rule.id": rule_id}},
                    {"match": {"agent.id": AGENT_ID}},
                    {"range": {"timestamp": {"gte": "now-1h"}}}
                ]
            }
        },
        "size": 1
    }
    try:
        response = requests.post(
            "https://localhost:9200/wazuh-alerts-*/_search",
            headers=headers,
            json=query,
            verify=False,
            timeout=10,
            auth=("admin", "SecretPassword")
        )
        if response.status_code == 200:
            hits = response.json().get("hits", {}).get("total", {}).get("value", 0)
            return hits > 0
        else:
            print(f"    [-] Index query failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"    [-] Query error: {e}")
        return False

def run_validation():
    """Main validation pipeline"""
    print("=" * 60)
    print("  Detection Engineering CI/CD Pipeline")
    print(f"  Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Authenticate to Wazuh API
    token = get_wazuh_token()
    if not token:
        print("[-] Cannot connect to Wazuh API.")
        return

    results = []
    passed = 0
    failed = 0

    for technique in TECHNIQUES:
        print(f"\n[*] Testing {technique['id']} - {technique['name']}")
        print(f"    Tactic: {technique['tactic']}")
        print(f"    Expected Rule: {technique['custom_rule_id']}")

        time.sleep(2)
        fired = check_rule_fired(token, technique['custom_rule_id'])

        if fired:
            status = "PASS"
            passed += 1
            print(f"    [✓] PASS - Rule {technique['custom_rule_id']} confirmed in alerts!")
        else:
            status = "FAIL"
            failed += 1
            print(f"    [✗] FAIL - Rule {technique['custom_rule_id']} not found in alerts")

        results.append({
            "technique_id": technique["id"],
            "technique_name": technique["name"],
            "tactic": technique["tactic"],
            "rule_id": technique["custom_rule_id"],
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    # Summary
    print("\n" + "=" * 60)
    print("  DETECTION COVERAGE REPORT")
    print("=" * 60)
    print(f"  Total Techniques Tested: {len(TECHNIQUES)}")
    print(f"  Passed:   {passed}")
    print(f"  Failed:   {failed}")
    coverage = (passed / len(TECHNIQUES)) * 100
    print(f"  Coverage: {coverage:.1f}%")
    print("=" * 60)

    report = {
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total": len(TECHNIQUES),
            "passed": passed,
            "failed": failed,
            "coverage_percent": round(coverage, 1)
        },
        "results": results
    }

    report_file = f"reports/coverage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n[+] Report saved to {report_file}")
    return report

if __name__ == "__main__":
    run_validation()

#!/usr/bin/env python3
"""
AI-Powered SOC Incident Report Generator
Uses Claude API to generate a professional incident report
"""

import json
import glob
import os
import requests
import urllib3
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

def load_latest_report():
    reports = glob.glob("reports/coverage_*.json")
    if not reports:
        print("[-] No coverage reports found.")
        return None
    latest = max(reports, key=os.path.getctime)
    with open(latest) as f:
        return json.load(f)

def generate_ai_report(coverage_data):
    prompt = f"""You are a senior SOC analyst and detection engineer. Generate a professional incident report based on the following detection validation results from a CI/CD pipeline test.

Coverage Data:
{json.dumps(coverage_data, indent=2)}

Write a professional SOC incident report that includes:

1. EXECUTIVE SUMMARY
2. ATTACK SIMULATION OVERVIEW
3. DETECTION FINDINGS - for each technique tested
4. TECHNICAL ANALYSIS
5. RECOMMENDATIONS
6. CONCLUSION

Format as professional markdown. Be specific and technical. Use actual technique IDs and rule numbers from the data."""

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    body = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }

    print("[*] Generating AI incident report...")
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=body,
        timeout=60
    )

    if response.status_code == 200:
        report_text = response.json()["content"][0]["text"]
        output_file = f"reports/incident_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(output_file, "w") as f:
            f.write(report_text)
        print(f"[+] AI incident report saved to {output_file}")
        print("\n" + "="*60)
        print(report_text[:500] + "...")
        print("="*60)
        return output_file
    else:
        print(f"[-] API error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    report = load_latest_report()
    if report:
        generate_ai_report(report)

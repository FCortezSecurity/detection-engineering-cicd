#!/usr/bin/env python3
"""
ATT&CK Coverage Dashboard Generator
Generates a professional HTML coverage report
"""

import json
import glob
import os
from datetime import datetime

def load_latest_report():
    """Load the most recent coverage report"""
    reports = glob.glob("reports/coverage_*.json")
    if not reports:
        print("[-] No reports found. Run validate_detections.py first.")
        return None
    latest = max(reports, key=os.path.getctime)
    with open(latest) as f:
        return json.load(f)

def generate_dashboard(report):
    """Generate HTML dashboard from coverage report"""
    results = report["results"]
    summary = report["summary"]
    timestamp = report["run_timestamp"]

    # Build technique rows
    rows = ""
    for r in results:
        status_class = "pass" if r["status"] == "PASS" else "fail"
        status_icon = "✓" if r["status"] == "PASS" else "✗"
        rows += f"""
        <tr>
            <td><span class="technique-id">{r['technique_id']}</span></td>
            <td>{r['technique_name']}</td>
            <td><span class="tactic">{r['tactic']}</span></td>
            <td><span class="rule-id">#{r['rule_id']}</span></td>
            <td><span class="status {status_class}">{status_icon} {r['status']}</span></td>
        </tr>"""

    coverage = summary["coverage_percent"]
    color = "#00ff88" if coverage == 100 else "#ffaa00" if coverage >= 60 else "#ff4444"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Detection Engineering CI/CD - Coverage Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Courier New', monospace;
            background: #0a0e1a;
            color: #c9d1d9;
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        .header {{
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 30px;
            background: #0d1117;
            text-align: center;
        }}
        .header h1 {{
            font-size: 1.8em;
            color: #58a6ff;
            margin-bottom: 10px;
            letter-spacing: 2px;
        }}
        .header .subtitle {{
            color: #8b949e;
            font-size: 0.9em;
        }}
        .coverage-ring {{
            margin: 30px auto;
            width: 160px;
            height: 160px;
            position: relative;
        }}
        .coverage-ring svg {{ transform: rotate(-90deg); }}
        .coverage-ring .percentage {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 2em;
            font-weight: bold;
            color: {color};
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin: 20px 0;
        }}
        .stat {{
            text-align: center;
        }}
        .stat .number {{
            font-size: 2em;
            font-weight: bold;
        }}
        .stat .label {{
            color: #8b949e;
            font-size: 0.8em;
            text-transform: uppercase;
        }}
        .pass-num {{ color: #00ff88; }}
        .fail-num {{ color: #ff4444; }}
        .total-num {{ color: #58a6ff; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            overflow: hidden;
        }}
        th {{
            background: #161b22;
            color: #58a6ff;
            padding: 14px 16px;
            text-align: left;
            font-size: 0.8em;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid #30363d;
        }}
        td {{
            padding: 14px 16px;
            border-bottom: 1px solid #21262d;
            font-size: 0.9em;
        }}
        tr:last-child td {{ border-bottom: none; }}
        tr:hover td {{ background: #161b22; }}
        .technique-id {{
            color: #ff7b72;
            font-weight: bold;
        }}
        .tactic {{
            background: #1f2937;
            color: #93c5fd;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.8em;
        }}
        .rule-id {{
            color: #d2a8ff;
            font-family: monospace;
        }}
        .status {{
            padding: 4px 12px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.85em;
        }}
        .status.pass {{
            background: #0d2818;
            color: #00ff88;
            border: 1px solid #00ff88;
        }}
        .status.fail {{
            background: #2d1018;
            color: #ff4444;
            border: 1px solid #ff4444;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #8b949e;
            font-size: 0.8em;
        }}
        .mitre-badge {{
            display: inline-block;
            background: #1a1f2e;
            border: 1px solid #58a6ff;
            color: #58a6ff;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 0.8em;
            margin: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ DETECTION ENGINEERING CI/CD</h1>
            <p class="subtitle">ATT&CK Coverage Validation Report</p>
            <p class="subtitle">Generated: {timestamp}</p>

            <div class="coverage-ring">
                <svg width="160" height="160" viewBox="0 0 160 160">
                    <circle cx="80" cy="80" r="70"
                        fill="none" stroke="#21262d" stroke-width="12"/>
                    <circle cx="80" cy="80" r="70"
                        fill="none" stroke="{color}" stroke-width="12"
                        stroke-dasharray="{2 * 3.14159 * 70 * coverage / 100:.1f} {2 * 3.14159 * 70:.1f}"
                        stroke-linecap="round"/>
                </svg>
                <div class="percentage">{coverage:.0f}%</div>
            </div>

            <div class="stats">
                <div class="stat">
                    <div class="number total-num">{summary['total']}</div>
                    <div class="label">Total</div>
                </div>
                <div class="stat">
                    <div class="number pass-num">{summary['passed']}</div>
                    <div class="label">Passed</div>
                </div>
                <div class="stat">
                    <div class="number fail-num">{summary['failed']}</div>
                    <div class="label">Failed</div>
                </div>
            </div>

            <div>
                <span class="mitre-badge">T1057 Discovery</span>
                <span class="mitre-badge">T1059.001 Execution</span>
                <span class="mitre-badge">T1082 Discovery</span>
                <span class="mitre-badge">T1053.005 Persistence</span>
                <span class="mitre-badge">T1027 Defense Evasion</span>
            </div>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Technique ID</th>
                    <th>Technique Name</th>
                    <th>Tactic</th>
                    <th>Rule ID</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>

        <div class="footer">
            <p>Detection Engineering CI/CD Platform | Wazuh + Sysmon + Atomic Red Team</p>
            <p>MITRE ATT&CK Framework | Windows 11 Target | Custom Detection Rules</p>
        </div>
    </div>
</body>
</html>"""

    output_file = f"reports/dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(output_file, "w") as f:
        f.write(html)
    print(f"[+] Dashboard saved to {output_file}")
    return output_file

if __name__ == "__main__":
    report = load_latest_report()
    if report:
        generate_dashboard(report)

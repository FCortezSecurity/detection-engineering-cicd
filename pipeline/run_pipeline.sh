#!/bin/bash
echo "============================================"
echo "  Detection Engineering CI/CD Pipeline"
echo "  Full Run - $(date)"
echo "============================================"

echo ""
echo "[1/3] Running detection validation..."
python3 pipeline/validate_detections.py

echo ""
echo "[2/3] Generating coverage dashboard..."
python3 pipeline/generate_dashboard.py

echo ""
echo "[3/3] Generating AI incident report..."
python3 pipeline/generate_report.py

echo ""
echo "============================================"
echo "  Pipeline complete!"
echo "  Check reports/ folder for all outputs"
echo "============================================"

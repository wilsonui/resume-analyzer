#!/bin/bash
# run.sh — Quick start script for Smart Resume Analyzer

echo "╔════════════════════════════════════════════╗"
echo "║       Smart Resume Analyzer — Setup        ║"
echo "╚════════════════════════════════════════════╝"

# 1. Create virtual environment
echo ""
echo "▶ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
echo "▶ Installing dependencies..."
pip install --upgrade pip -q
pip install Flask==3.0.0 Werkzeug==3.0.1 PyPDF2==3.0.1 python-docx==1.1.0 \
    scikit-learn==1.4.0 numpy==1.26.3 pandas==2.1.4 -q

echo ""
echo "▶ All dependencies installed!"
echo ""
echo "▶ Starting application on http://localhost:5000"
echo ""
python app.py

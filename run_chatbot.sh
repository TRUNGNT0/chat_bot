#!/bin/bash

echo "========================================"
echo "  Setup & Configuration Chatbot"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python3 is not installed"
    exit 1
fi

echo "[1/3] Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "[2/3] Running Streamlit app..."
echo ""
echo "Opening browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run chatbot_app.py

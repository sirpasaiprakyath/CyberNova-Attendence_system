#!/bin/bash

# Hackathon Attendance System - Quick Start Script

echo ""
echo "============================================================"
echo "HACKATHON ATTENDANCE SYSTEM - Quick Start"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.8 or higher."
    echo "Install with: brew install python3 (macOS) or apt install python3 (Linux)"
    exit 1
fi

echo "[✓] Python detected: $(python3 --version)"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "[•] Creating virtual environment..."
    python3 -m venv venv
    echo "[✓] Virtual environment created"
    echo ""
fi

# Activate venv
echo "[•] Activating virtual environment..."
source venv/bin/activate
echo "[✓] Virtual environment activated"
echo ""

# Install requirements
echo "[•] Installing dependencies..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies."
    exit 1
fi
echo "[✓] Dependencies installed"
echo ""

# Run the application
echo "[•] Starting Hackathon Attendance System..."
echo ""
python app.py

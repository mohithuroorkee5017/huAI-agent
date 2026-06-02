#!/bin/bash

# HUVOICE AGENT - Unix/Linux Startup Script

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  HUVOICE AGENT - Startup              ║"
echo "║  Advanced Voice-Based AI Assistant     ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ using:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi

echo "[INFO] Python detected"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "[INFO] Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "[INFO] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

echo "[INFO] Dependencies are ready"
echo ""

# Start the application
echo "[INFO] Starting HUVOICE AGENT..."
echo ""
echo "╔════════════════════════════════════════╗"
echo "║  HUVOICE AGENT is starting...         ║"
echo "║  Web Interface: http://localhost:5000  ║"
echo "║  Press Ctrl+C to stop                  ║"
echo "╚════════════════════════════════════════╝"
echo ""

python huvoice_agent.py

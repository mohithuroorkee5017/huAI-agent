#!/bin/bash

# HU Voice AI API - Startup Script for Linux/macOS

echo ""
echo "========================================"
echo "HU Voice AI API - Starting Server"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing/updating dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and configure your OpenRouter API key:"
    echo ""
    echo "OPENROUTER_API_KEY=your_api_key_here"
    echo ""
    read -p "Press Enter to create .env from .env.example..."
    cp .env.example .env
fi

# Start the server
echo ""
echo "========================================"
echo "Starting HU Voice AI API Server..."
echo "========================================"
echo ""
echo "Server running at: http://localhost:5000"
echo "API Docs at: http://localhost:5000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py

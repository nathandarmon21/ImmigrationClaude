#!/bin/bash

# Immigration Advisory Backend Startup Script

echo "Starting Immigration Advisory System Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and add your Anthropic API key"
    exit 1
fi

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

# Run the server
echo "Starting FastAPI server..."
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

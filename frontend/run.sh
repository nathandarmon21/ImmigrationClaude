#!/bin/bash

# Immigration Advisory Frontend Startup Script

echo "Starting Immigration Advisory System Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    echo "VITE_API_URL=http://localhost:8000" > .env.local
fi

# Start development server
echo "Starting Vite development server..."
npm run dev

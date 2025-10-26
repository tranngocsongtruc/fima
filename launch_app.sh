#!/bin/bash
# Smart File Organizer - Simple Launcher
# This script launches the app and opens the browser

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║        Smart File Organizer - CalHacks 12                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo ""
    echo "Please create a .env file with your API keys:"
    echo "  cp .env.example .env"
    echo "  # Then edit .env with your Claude API key"
    echo ""
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements-core.txt
fi

echo "🚀 Starting Smart File Organizer..."
echo ""

# Start the server in background
python3 backend/main.py &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Open browser
echo "🌐 Opening web interface..."
open http://127.0.0.1:8000

echo ""
echo "✅ App is running!"
echo "   • Web UI: http://127.0.0.1:8000"
echo "   • Press Ctrl+C to stop"
echo ""

# Wait for user to stop
wait $SERVER_PID

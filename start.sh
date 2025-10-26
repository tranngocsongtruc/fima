#!/bin/bash

# Smart File Organizer - Startup Script
# CalHacks 12 - October 2025

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║        Smart File Organizer - CalHacks 12                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "📝 Please edit .env and add your API keys:"
    echo "   - GROQ_API_KEY (get at https://console.groq.com)"
    echo "   - ANTHROPIC_API_KEY (get at https://console.anthropic.com)"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create data directory
mkdir -p data

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Smart File Organizer..."
echo ""

# Start the backend server
cd backend
python main.py

#!/bin/bash
# Quick start script for running downloader on server

set -e

echo "=================================="
echo "🚀 Starting Stone Classifier Downloader"
echo "=================================="

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if .env file exists
if [ -f ".env" ]; then
    echo "🔑 Loading environment variables from .env..."
    source .env
else
    echo "⚠️  No .env file found. Using environment variables if set."
fi

# Check API key
if [ -z "$PEXELS_API_KEY" ]; then
    echo ""
    echo "❌ ERROR: PEXELS_API_KEY not set!"
    echo "   Please either:"
    echo "   1. Create .env file from template: cp .env.template .env"
    echo "   2. Or export manually: export PEXELS_API_KEY='your_key'"
    exit 1
fi

echo "✅ API key configured"
echo ""
echo "🎯 Starting download in background..."

# Run in background with nohup
nohup python download_images.py > download_log.txt 2>&1 &

PID=$!
echo "✅ Started! PID: $PID"
echo ""
echo "📝 Monitor progress with:"
echo "   tail -f download_log.txt"
echo "   # OR"
echo "   bash monitor_downloads.sh"
echo ""
echo "🛑 Stop with:"
echo "   pkill -f download_images.py"
echo ""

#!/bin/bash
# Startup script for Python Boyce application

set -e

echo "🚀 Starting Python Boyce - 12-Factor App"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Load environment variables if .env exists
if [ -f ".env" ]; then
    echo "⚙️  Loading environment variables from .env..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  No .env file found. Using defaults..."
    export DEBUG=True
    export ENVIRONMENT=development
    export DATABASE_URL=sqlite:///dev.db
    export REDIS_URL=redis://localhost:6379
    export PORT=5000
fi

# Show application status
echo "📊 Application Status:"
python3 manage.py status

echo ""
echo "🌐 Starting web server on port ${PORT:-5000}..."
echo "   Visit: http://localhost:${PORT:-5000}"
echo "   Health: http://localhost:${PORT:-5000}/health"
echo "   Config: http://localhost:${PORT:-5000}/config"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the application
python3 app.py
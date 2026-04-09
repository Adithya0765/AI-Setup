#!/bin/bash

# NEXUS Setup Script
# This script sets up NEXUS on your system

set -e

echo "🚀 NEXUS Setup"
echo "=============="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.9+ required. Found: $python_version"
    exit 1
fi
echo "✓ Python $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"
echo ""

# Install NEXUS
echo "Installing NEXUS..."
pip install -e . > /dev/null 2>&1
echo "✓ NEXUS installed"
echo ""

# Setup configuration
echo "Setting up configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys:"
    echo "   - GEMINI_API_KEYS=your_key_here"
    echo "   - GROK_API_KEYS=your_key_here"
    echo ""
else
    echo "✓ .env file exists"
    echo ""
fi

# Create directories
echo "Creating directories..."
mkdir -p .nexus/memory
mkdir -p .nexus/strategies
mkdir -p .nexus/logs
echo "✓ Directories created"
echo ""

# Test installation
echo "Testing installation..."
if python -c "from nexus.orchestrator import Orchestrator; print('OK')" 2>/dev/null; then
    echo "✓ Installation successful"
else
    echo "❌ Installation test failed"
    exit 1
fi
echo ""

# Show next steps
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Activate the environment: source venv/bin/activate"
echo "3. Run NEXUS: python -m nexus \"your task here\""
echo ""
echo "Documentation:"
echo "- Quick start: cat QUICKSTART.md"
echo "- Architecture: cat ARCHITECTURE.md"
echo "- Testing: cat TESTING.md"
echo ""
echo "Happy coding! 🎉"

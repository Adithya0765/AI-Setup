#!/bin/bash
# Test script to verify NEXUS installation

echo "🧪 Testing NEXUS Installation"
echo "=============================="
echo ""

# Test 1: Check if nexus command exists
echo "Test 1: Command availability"
if command -v nexus &> /dev/null; then
    echo "✅ 'nexus' command found"
else
    echo "❌ 'nexus' command not found"
    echo "   Make sure ~/.local/bin is in your PATH"
fi
echo ""

# Test 2: Check config file
echo "Test 2: Configuration file"
if [ -f "$HOME/.nexus/config.env" ]; then
    echo "✅ Config file exists at ~/.nexus/config.env"
else
    echo "❌ Config file not found"
fi
echo ""

# Test 3: Check installation directory
echo "Test 3: Installation directory"
if [ -d "$HOME/.nexus/nexus" ]; then
    echo "✅ NEXUS installed at ~/.nexus/"
else
    echo "❌ Installation directory not found"
fi
echo ""

# Test 4: Check virtual environment
echo "Test 4: Virtual environment"
if [ -d "$HOME/.nexus/venv" ]; then
    echo "✅ Virtual environment exists"
else
    echo "❌ Virtual environment not found"
fi
echo ""

# Test 5: Test import
echo "Test 5: Python imports"
if "$HOME/.nexus/venv/bin/python" -c "from nexus.orchestrator import Orchestrator; print('OK')" 2>/dev/null; then
    echo "✅ Python imports working"
else
    echo "❌ Import test failed"
fi
echo ""

# Test 6: Check for API keys
echo "Test 6: API key configuration"
if grep -q "NEXUS_PRIMARY_KEYS=.\+" "$HOME/.nexus/config.env" 2>/dev/null; then
    echo "✅ Primary keys configured"
else
    echo "⚠️  Primary keys not configured"
    echo "   Edit ~/.nexus/config.env and add your keys"
fi

if grep -q "NEXUS_SECONDARY_KEYS=.\+" "$HOME/.nexus/config.env" 2>/dev/null; then
    echo "✅ Secondary keys configured"
else
    echo "⚠️  Secondary keys not configured"
    echo "   Edit ~/.nexus/config.env and add your keys"
fi
echo ""

# Summary
echo "=============================="
echo "Test complete!"
echo ""
echo "If all tests passed, try:"
echo "  nexus \"test task\""
echo ""
echo "If tests failed, run the installer again:"
echo "  ./install.sh"

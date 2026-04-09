#!/bin/bash
# NEXUS Installer for Linux/Mac
# Usage: curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/nexus/main/install.sh | bash

set -e

REPO_URL="https://github.com/YOUR_USERNAME/nexus"  # TODO: Update with your GitHub username
INSTALL_DIR="$HOME/.nexus"
BIN_DIR="$HOME/.local/bin"

echo ""
echo "╔════════════════════════════════════════╗"
echo "║   NEXUS - AI Coding Assistant          ║"
echo "║   Self-Evolving Intelligence           ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check Python
echo "🔍 Checking requirements..."
if ! command -v python3 &> /dev/null; then
    echo "  ❌ Python 3.9+ is required"
    echo "     Install from: https://www.python.org/downloads/"
    exit 1
fi
echo "  ✓ Python found: $(python3 --version)"

# Check Git
if ! command -v git &> /dev/null; then
    echo "  ❌ Git is required"
    echo "     Install with: sudo apt install git (Ubuntu/Debian)"
    echo "                   brew install git (Mac)"
    exit 1
fi
echo "  ✓ Git found"

# Create directories
echo ""
echo "📦 Setting up installation..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
echo "  ✓ Created directories"

# Clone repository
echo ""
echo "📥 Downloading NEXUS..."
if [ -d "$INSTALL_DIR/nexus" ]; then
    echo "  Removing old installation..."
    rm -rf "$INSTALL_DIR/nexus"
fi

cd "$INSTALL_DIR"
if ! git clone --depth 1 "$REPO_URL" nexus-repo > /dev/null 2>&1; then
    echo "  ❌ Failed to download NEXUS"
    echo "     Make sure the repository is public"
    exit 1
fi
echo "  ✓ Downloaded successfully"

# Move files
mv "$INSTALL_DIR/nexus-repo/"* "$INSTALL_DIR/"
mv "$INSTALL_DIR/nexus-repo/".* "$INSTALL_DIR/" 2>/dev/null || true
rm -rf "$INSTALL_DIR/nexus-repo"

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"
echo "  ✓ Virtual environment created"

# Install dependencies
echo ""
echo "📚 Installing dependencies..."
source "$INSTALL_DIR/venv/bin/activate"
pip install --upgrade pip --quiet
pip install -r "$INSTALL_DIR/requirements.txt" --quiet
pip install -e "$INSTALL_DIR" --quiet
echo "  ✓ Dependencies installed"

# Create executable wrapper
echo ""
echo "🔗 Creating nexus command..."
cat > "$BIN_DIR/nexus" << 'EOF'
#!/bin/bash
source "$HOME/.nexus/venv/bin/activate"
python -m nexus "$@"
EOF

chmod +x "$BIN_DIR/nexus"
echo "  ✓ Command created"

# Add to PATH if needed
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo "⚙️  Updating PATH..."
    
    # Detect shell
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.profile"
    fi
    
    # Add to shell config
    if ! grep -q ".local/bin" "$SHELL_RC" 2>/dev/null; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        echo "  ✓ Added to $SHELL_RC"
    fi
fi

echo ""
echo "╔════════════════════════════════════════╗"
echo "║   ✅ Installation Complete!            ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "🎉 NEXUS is ready to use!"
echo ""
echo "Next steps:"
echo "  1. Restart your terminal (or run: source ~/.bashrc)"
echo "  2. Run: nexus --status"
echo "  3. Try: nexus \"list all Python files\""
echo ""
echo "📚 Documentation: https://docs.nexus.ai"
echo "💬 Support: support@nexus.ai"
echo ""

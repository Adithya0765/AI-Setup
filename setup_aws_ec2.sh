#!/bin/bash
# Run this script ON your EC2 instance after first login
# It sets up everything automatically

echo "🚀 Setting up Marketing AI on AWS EC2..."

# Update system
echo "📦 Updating system packages..."
sudo apt update

# Install git-lfs
echo "📦 Installing git-lfs..."
sudo apt install git-lfs -y
git lfs install

# Check if CUDA is available
echo "🔍 Checking GPU..."
nvidia-smi

# Setup Python environment
echo "🐍 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

# Install requirements
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Login to HuggingFace
echo "🤗 Please login to HuggingFace..."
echo "Get your token from: https://huggingface.co/settings/tokens"
huggingface-cli login

# Download models
echo "📥 Downloading models (~57GB, takes 10-20 minutes)..."
python setup_base_models.py

# Setup auto-shutdown (optional)
echo "⏰ Setting up auto-shutdown after 30 minutes of inactivity..."
nohup python aws_auto_shutdown.py > auto_shutdown.log 2>&1 &

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Test generation: python router_system.py"
echo "2. When done, STOP the instance to save money!"
echo "3. Stop command: sudo shutdown -h now"
echo ""
echo "💰 Cost tracking:"
echo "   - g5.xlarge spot: ~$0.35/hour"
echo "   - Your $185 = ~528 hours"
echo "   - ALWAYS stop when not using!"

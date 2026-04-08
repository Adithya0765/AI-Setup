# AWS EC2 Setup Guide for Marketing AI

## Step 1: Launch EC2 Spot Instance

### 1.1 Go to AWS Console
- Login to AWS Console: https://console.aws.amazon.com
- Go to EC2 Dashboard
- Click "Launch Instance"

### 1.2 Configure Instance

**Name:** marketing-ai-gpu

**AMI (Operating System):**
- Search for: "Deep Learning AMI GPU PyTorch" 
- Select: Deep Learning AMI GPU PyTorch 2.1.0 (Ubuntu 20.04)
- This comes with CUDA, PyTorch pre-installed!

**Instance Type:**
- Click "Compare instance types"
- Filter by: g5.xlarge or g5.2xlarge
- Select: **g5.xlarge** (24GB GPU, cheaper)

**Key Pair:**
- Create new key pair
- Name: marketing-ai-key
- Type: RSA
- Format: .pem (for SSH)
- Download and save it!

**Network Settings:**
- Allow SSH (port 22) from your IP
- Allow HTTPS (port 443)
- Allow Custom TCP (port 8888) for Jupyter

**Storage:**
- 200 GB gp3 (for models)

**Advanced Details - IMPORTANT:**
- Scroll down to "Purchasing option"
- ✅ CHECK "Request Spot Instances"
- Maximum price: $0.50/hour (default is fine)
- Interruption behavior: Stop (not terminate)

### 1.3 Launch
- Click "Launch Instance"
- Wait 2-3 minutes for it to start

## Step 2: Connect to Instance

### 2.1 Get Connection Info
- Go to EC2 Dashboard > Instances
- Select your instance
- Click "Connect"
- Copy the SSH command

### 2.2 Connect via SSH

**On Windows (PowerShell):**
```powershell
# Navigate to where you saved the key
cd "C:\path\to\your\key"

# Set permissions (if needed)
icacls marketing-ai-key.pem /inheritance:r
icacls marketing-ai-key.pem /grant:r "%username%:R"

# Connect
ssh -i marketing-ai-key.pem ubuntu@YOUR_INSTANCE_IP
```

**On Mac/Linux:**
```bash
chmod 400 marketing-ai-key.pem
ssh -i marketing-ai-key.pem ubuntu@YOUR_INSTANCE_IP
```

## Step 3: Setup Environment

Once connected, run these commands:

```bash
# Update system
sudo apt update

# Install git-lfs for large files
sudo apt install git-lfs -y
git lfs install

# Clone your repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Login to HuggingFace
huggingface-cli login
# Paste your token: hf_your_token_here
```

## Step 4: Download Models

```bash
# Download all models to EC2
python setup_base_models.py
```

This downloads ~57GB. Takes 10-20 minutes on EC2's fast network.

## Step 5: Test Generation

```bash
# Run the router system
python router_system.py
```

## Step 6: IMPORTANT - Stop Instance When Not Using

**To save money, ALWAYS stop the instance when not generating:**

```bash
# From your local machine
aws ec2 stop-instances --instance-ids YOUR_INSTANCE_ID
```

Or from AWS Console:
- EC2 Dashboard > Instances
- Select instance
- Instance State > Stop

**To start again:**
```bash
aws ec2 start-instances --instance-ids YOUR_INSTANCE_ID
```

## Cost Tracking

**Monitor your spending:**
- AWS Console > Billing Dashboard
- Set up billing alerts at $50, $100, $150

**Estimated costs:**
- g5.xlarge spot: ~$0.35/hour
- $185 = ~528 hours
- Generate 10 images/hour = 5,280 images total

## Tips to Save Money

1. **Stop instance when not using** (most important!)
2. Use spot instances (you already are)
3. Generate in batches (don't keep running for single images)
4. Delete instance when done (keep models in S3)
5. Use smaller instance for testing (t2.micro is free tier)

## Backup Plan if Spot Instance Interrupted

Spot instances can be interrupted if AWS needs capacity. If this happens:
- Your instance will STOP (not terminate)
- Just start it again
- Models are still there
- Very rare for g5 instances

## Next Steps

1. Launch instance
2. Connect via SSH  
3. Download models
4. Start generating!
5. Get your first client
6. Use their money for more GPU time

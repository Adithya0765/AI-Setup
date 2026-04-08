# Marketing AI Model Stack

State-of-the-art image, video, and audio generation models for automated marketing content.

## Models

- **Image**: FLUX.1-dev (12B params)
- **Video**: LTX-Video (4K, 60s, synchronized audio)
- **Audio**: Fish Speech V1.5 (multilingual)
- **Router**: Mistral 7B (intelligent routing)

## RECOMMENDED: AWS EC2 with Spot Instances (Best Value!)

### Why AWS EC2?
- g5.xlarge spot: ~$0.35/hour (70% cheaper than on-demand)
- 24GB GPU (A10G) - runs all models
- Your $185 = 460-600 hours of GPU time
- Pay only when running
- Stop anytime to save money

### Quick Start

See **[aws_setup_guide.md](aws_setup_guide.md)** for detailed instructions.

**Summary:**
1. Launch g5.xlarge spot instance with Deep Learning AMI
2. SSH into instance
3. Run: `bash setup_aws_ec2.sh`
4. Generate content!
5. **STOP instance when done** (saves money!)

**Manage from local machine:**
```bash
# Edit aws_ec2_manager.sh with your instance ID
chmod +x aws_ec2_manager.sh

# Start instance
./aws_ec2_manager.sh start

# Connect
./aws_ec2_manager.sh connect

# Stop (IMPORTANT!)
./aws_ec2_manager.sh stop
```

---

## ALTERNATIVE: Use Modal + Your HuggingFace Account

### Step 1: Setup

```bash
# Install Modal
pip install modal

# Create Modal account (opens browser)
modal token new

# Add your HuggingFace token to Modal (needs WRITE access)
modal secret create huggingface-secret HF_TOKEN=hf_your_token_here
```

Get your HF token from: https://huggingface.co/settings/tokens (make sure it has WRITE permission)

### Step 2: Copy Models to YOUR HuggingFace Account (One-time)

```bash
# Use Modal's fast network to copy models to your HF account
modal run modal_copy_to_hf.py --username YOUR_HF_USERNAME
```

Replace `YOUR_HF_USERNAME` with your actual HuggingFace username.

This copies ~57GB of models using Modal's datacenter network (10-20 minutes):
- FLUX.1-dev → `your-username/FLUX.1-dev`
- LTX-Video → `your-username/LTX-Video`
- Fish Speech V1.5 → `your-username/fish-speech-1.5`
- Mistral 7B → `your-username/Mistral-7B-Instruct-v0.2`

Now you OWN these models in your HF account!

### Step 3: Deploy Inference System

```bash
# Deploy inference that uses YOUR models
modal deploy modal_inference_from_hf.py
```

### Step 4: Generate Content

```bash
# Generate using YOUR models
modal run modal_inference_from_hf.py --username YOUR_HF_USERNAME --request "Create a professional product photo for a smartphone"

# More examples
modal run modal_inference_from_hf.py --username YOUR_HF_USERNAME --request "Social media ad for energy drink"
modal run modal_inference_from_hf.py --username YOUR_HF_USERNAME --request "Product demo video for wireless headphones"
```

## Architecture

```
User Request
    ↓
Mistral Router (Langflow)
    ↓
┌───────────┬──────────────┬─────────────┐
│   FLUX    │  LTX Video   │ Fish Speech │
│  (Image)  │   (Video)    │   (Audio)   │
└───────────┴──────────────┴─────────────┘
    ↓
Content Compositor
    ↓
Final Marketing Asset
```

## Next Steps

1. Prepare your training datasets (images, videos, audio)
2. Run the download script to copy models to your HF account
3. Set up Modal and deploy the fine-tuning functions
4. Fine-tune each model on your marketing content
5. Set up Langflow for orchestration

## Notes

- FLUX.1-dev is the open-source version (FLUX.2 Pro is API-only)
- LTX-2.3 supports native audio generation
- Fish Speech V1.5 has best quality for voiceovers
- All models support LoRA fine-tuning for efficiency


## Usage Examples

```python
from router_system import MarketingRouter

router = MarketingRouter()

# Example 1: Social media ad
results = router.generate_content(
    "Create a vibrant Instagram ad for a new energy drink"
)

# Example 2: Product video
results = router.generate_content(
    "Generate a 30-second product demo video for wireless headphones with voiceover"
)

# Example 3: Just an image
results = router.generate_content(
    "Professional product photo of a smartwatch on a marble surface"
)
```

## Architecture

```
User Request
    ↓
Mistral Router (analyzes request)
    ↓
Decides: Image? Video? Audio?
    ↓
┌───────────┬──────────────┬─────────────┐
│   FLUX    │  LTX Video   │ Fish Speech │
│  (Image)  │   (Video)    │   (Audio)   │
└───────────┴──────────────┴─────────────┘
    ↓
Generated Content
```

## Costs

### Local (Your GPU):
- Free (but requires powerful GPU: RTX 4090 or better)
- ~57GB disk space

### Modal (Cloud):
- A100 GPU: ~$1-3/hour
- Only pay when generating
- No upfront costs

## When to Fine-tune?

Start with base models. Fine-tune only if:
- Client needs consistent brand style
- Base models don't match desired output
- You have 20+ high-quality examples

See `modal_finetune_setup.py` for fine-tuning instructions.

## Troubleshooting

**Out of memory?**
- Use Modal instead of local
- Reduce batch size
- Use smaller models

**Slow generation?**
- Modal is faster than local
- Models cache after first run
- Consider using FLUX.1-schnell (faster variant)

**Poor quality output?**
- Improve prompts (be specific)
- Adjust inference steps (50-100)
- Try different guidance scales (7-15)

#!/usr/bin/env python3
"""
Script to download and upload models to your HuggingFace account.
Run: python download_to_hf.py --model <model_name> --target <your_hf_username>
"""

import argparse
import subprocess
import os
from pathlib import Path

MODELS = {
    "flux2-pro": "black-forest-labs/FLUX.1-dev",  # FLUX.2 Pro is API-only, use FLUX.1-dev for fine-tuning
    "ltx-video": "Lightricks/LTX-Video",
    "fish-speech": "fishaudio/fish-speech-1.5",
    "cosyvoice": "FunAudioLLM/CosyVoice2-0.5B",
    "cogvideox": "THUDM/CogVideoX-5b",
    "wan-video": "Wan-AI/Wan-2.2",
}

def download_and_upload(model_key: str, target_repo: str):
    """Download model from HF and upload to your account."""
    
    if model_key not in MODELS:
        print(f"Unknown model: {model_key}")
        print(f"Available models: {', '.join(MODELS.keys())}")
        return
    
    source_repo = MODELS[model_key]
    print(f"📥 Downloading {source_repo}...")
    
    # Create temp directory
    temp_dir = Path(f"./temp_{model_key}")
    temp_dir.mkdir(exist_ok=True)
    
    # Clone the model
    try:
        subprocess.run([
            "git", "lfs", "install"
        ], check=True)
        
        subprocess.run([
            "git", "clone",
            f"https://huggingface.co/{source_repo}",
            str(temp_dir / model_key)
        ], check=True)
        
        print(f"✅ Downloaded to {temp_dir / model_key}")
        
        # Upload to your repo
        print(f"📤 Uploading to {target_repo}/{model_key}...")
        
        os.chdir(temp_dir / model_key)
        
        subprocess.run([
            "git", "remote", "set-url", "origin",
            f"https://huggingface.co/{target_repo}/{model_key}"
        ], check=True)
        
        subprocess.run([
            "git", "push", "-u", "origin", "main"
        ], check=True)
        
        print(f"✅ Uploaded to {target_repo}/{model_key}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Installed git-lfs: https://git-lfs.github.com/")
        print("2. Logged in to HuggingFace: huggingface-cli login")
        print("3. Created the target repo on HuggingFace")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download models to your HuggingFace account")
    parser.add_argument("--model", required=True, choices=list(MODELS.keys()), 
                       help="Model to download")
    parser.add_argument("--target", required=True, 
                       help="Your HuggingFace username (e.g., username)")
    
    args = parser.parse_args()
    download_and_upload(args.model, args.target)

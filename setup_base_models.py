"""
Setup script to download base models (no fine-tuning)
Run: python setup_base_models.py
"""

from huggingface_hub import snapshot_download
import os

def download_model(repo_id, local_dir):
    """Download model from HuggingFace"""
    print(f"📥 Downloading {repo_id}...")
    snapshot_download(
        repo_id=repo_id,
        local_dir=local_dir,
        local_dir_use_symlinks=False
    )
    print(f"✅ Downloaded to {local_dir}")

if __name__ == "__main__":
    # Create models directory
    os.makedirs("./models", exist_ok=True)
    
    print("Downloading base models (this will take a while)...\n")
    
    # Image model - FLUX.1-dev (12B params, ~24GB)
    download_model(
        "black-forest-labs/FLUX.1-dev",
        "./models/flux-dev"
    )
    
    # Video model - LTX-Video (~14GB)
    download_model(
        "Lightricks/LTX-Video",
        "./models/ltx-video"
    )
    
    # Audio model - Fish Speech V1.5 (~5GB)
    download_model(
        "fishaudio/fish-speech-1.5",
        "./models/fish-speech"
    )
    
    # Router model - Mistral 7B (~14GB)
    download_model(
        "mistralai/Mistral-7B-Instruct-v0.2",
        "./models/mistral-7b"
    )
    
    print("\n✅ All models downloaded!")
    print("Total size: ~57GB")

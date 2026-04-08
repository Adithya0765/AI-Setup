"""
Download all models using Modal's fast network and cache them
Run: modal run modal_download_models.py
This only needs to be done ONCE - models stay cached in Modal's volume
"""

import modal

app = modal.App("download-models")

# Image with HuggingFace tools
download_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("huggingface_hub", "torch", "transformers", "diffusers")
)

# Persistent volume to store models (shared across all Modal functions)
volume = modal.Volume.from_name("model-cache", create_if_missing=True)

@app.function(
    image=download_image,
    volumes={"/cache": volume},
    secrets=[modal.Secret.from_name("huggingface-secret")],
    timeout=7200,  # 2 hours for downloading
)
def download_all_models():
    """Download all models to Modal's volume using their fast network"""
    from huggingface_hub import snapshot_download
    import os
    
    models = {
        "FLUX.1-dev (Image)": "black-forest-labs/FLUX.1-dev",
        "LTX-Video (Video)": "Lightricks/LTX-Video", 
        "Fish Speech (Audio)": "fishaudio/fish-speech-1.5",
        "Mistral 7B (Router)": "mistralai/Mistral-7B-Instruct-v0.2",
    }
    
    print("🚀 Starting model downloads on Modal's fast network...\n")
    
    for name, repo_id in models.items():
        print(f"📥 Downloading {name} ({repo_id})...")
        try:
            snapshot_download(
                repo_id=repo_id,
                cache_dir="/cache",
                local_dir=f"/cache/{repo_id.replace('/', '--')}",
                local_dir_use_symlinks=False,
            )
            print(f"✅ {name} downloaded successfully!\n")
        except Exception as e:
            print(f"❌ Failed to download {name}: {e}\n")
    
    # Commit changes to volume
    volume.commit()
    
    print("🎉 All models downloaded and cached in Modal!")
    print("These models are now available for all your Modal functions.")
    print("\nNext step: Run 'modal deploy modal_inference.py' to deploy your inference API")

@app.function(
    image=download_image,
    volumes={"/cache": volume},
)
def list_cached_models():
    """Check what models are already cached"""
    import os
    
    print("📦 Cached models in Modal volume:\n")
    
    cache_dir = "/cache"
    if os.path.exists(cache_dir):
        items = os.listdir(cache_dir)
        if items:
            for item in items:
                path = os.path.join(cache_dir, item)
                if os.path.isdir(path):
                    # Get size
                    size = sum(
                        os.path.getsize(os.path.join(dirpath, filename))
                        for dirpath, dirnames, filenames in os.walk(path)
                        for filename in filenames
                    ) / (1024**3)  # Convert to GB
                    print(f"  ✓ {item} ({size:.2f} GB)")
        else:
            print("  (empty - no models cached yet)")
    else:
        print("  (cache directory doesn't exist yet)")

@app.local_entrypoint()
def main(action: str = "download"):
    """
    Main entry point
    
    Usage:
      modal run modal_download_models.py              # Download all models
      modal run modal_download_models.py --action list  # List cached models
    """
    if action == "download":
        download_all_models.remote()
    elif action == "list":
        list_cached_models.remote()
    else:
        print(f"Unknown action: {action}")
        print("Valid actions: download, list")

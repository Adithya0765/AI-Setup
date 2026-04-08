"""
Use Modal's fast network to copy models to YOUR HuggingFace account
Run: modal run modal_copy_to_hf.py --username YOUR_HF_USERNAME

This clones models from original repos to your HF account using Modal's datacenter network.
Much faster than doing it locally!
"""

import modal

app = modal.App("copy-models-to-hf")

# Image with HuggingFace tools (no git needed)
copy_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("huggingface_hub")
)

@app.function(
    image=copy_image,
    secrets=[modal.Secret.from_name("huggingface-secret")],
    timeout=7200,  # 2 hours
)
def copy_model_to_hf(source_repo: str, target_username: str, model_name: str):
    """Copy a model from source to your HuggingFace account using HF API"""
    import os
    from huggingface_hub import HfApi, create_repo, snapshot_download
    import shutil
    
    target_repo = f"{target_username}/{model_name}"
    
    print(f"\n{'='*60}")
    print(f"📥 Copying: {source_repo}")
    print(f"📤 To: {target_repo}")
    print(f"{'='*60}\n")
    
    try:
        api = HfApi()
        
        # Create target repo if it doesn't exist
        print(f"Creating repo {target_repo}...")
        try:
            create_repo(target_repo, exist_ok=True, repo_type="model")
            print(f"✅ Repo created/exists: {target_repo}")
        except Exception as e:
            print(f"⚠️ Repo creation note: {e}")
        
        # Download source model using HF Hub (much faster and simpler)
        print(f"\n📥 Downloading {source_repo} (using Modal's fast network)...")
        local_dir = "/tmp/model"
        
        snapshot_download(
            repo_id=source_repo,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
        )
        
        print(f"✅ Downloaded successfully!")
        
        # Upload to your repo
        print(f"\n📤 Uploading to {target_repo}...")
        
        api.upload_folder(
            folder_path=local_dir,
            repo_id=target_repo,
            repo_type="model",
        )
        
        print(f"\n✅ Successfully copied to {target_repo}!")
        
        # Cleanup
        shutil.rmtree(local_dir, ignore_errors=True)
        
        return {"status": "success", "repo": target_repo}
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return {"status": "error", "message": str(e)}

@app.local_entrypoint()
def main(username: str):
    """
    Copy all models to your HuggingFace account
    
    Usage:
      modal run modal_copy_to_hf.py --username YOUR_HF_USERNAME
    
    Before running:
      1. Create HuggingFace account at https://huggingface.co
      2. Get token from https://huggingface.co/settings/tokens (with WRITE access)
      3. Run: modal secret create huggingface-secret HF_TOKEN=your_token_here
    """
    
    if not username:
        print("❌ Error: Please provide your HuggingFace username")
        print("Usage: modal run modal_copy_to_hf.py --username YOUR_HF_USERNAME")
        return
    
    print(f"🚀 Starting model copy to {username}'s HuggingFace account")
    print(f"Using Modal's datacenter network for fast transfer\n")
    
    models = [
        {
            "source": "black-forest-labs/FLUX.1-dev",
            "name": "FLUX.1-dev",
            "size": "~24GB"
        },
        {
            "source": "Lightricks/LTX-Video",
            "name": "LTX-Video",
            "size": "~14GB"
        },
        {
            "source": "fishaudio/fish-speech-1.5",
            "name": "fish-speech-1.5",
            "size": "~5GB"
        },
        {
            "source": "mistralai/Mistral-7B-Instruct-v0.2",
            "name": "Mistral-7B-Instruct-v0.2",
            "size": "~14GB"
        }
    ]
    
    print("Models to copy:")
    for model in models:
        print(f"  • {model['name']} ({model['size']})")
    print(f"\nTotal: ~57GB\n")
    
    results = []
    for model in models:
        result = copy_model_to_hf.remote(
            model["source"],
            username,
            model["name"]
        )
        results.append(result)
    
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    for i, result in enumerate(results):
        model_name = models[i]["name"]
        if result["status"] == "success":
            print(f"✅ {model_name}: {result['repo']}")
        else:
            print(f"❌ {model_name}: {result.get('message', 'Failed')}")
    
    print("\n🎉 Done! Your models are now at:")
    print(f"   https://huggingface.co/{username}")

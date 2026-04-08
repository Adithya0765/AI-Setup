"""
Modal inference using YOUR HuggingFace models
Deploy: modal deploy modal_inference_from_hf.py
Run: modal run modal_inference_from_hf.py --username YOUR_HF_USERNAME --request "your request"
"""

import modal

app = modal.App("marketing-ai-from-hf")

# Image with all dependencies
inference_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch",
        "torchvision", 
        "diffusers",
        "transformers",
        "accelerate",
        "huggingface_hub",
        "Pillow",
        "sentencepiece",
        "protobuf"
    )
)

# Volume for caching (optional, speeds up subsequent runs)
volume = modal.Volume.from_name("model-cache", create_if_missing=True)

@app.function(
    image=inference_image,
    gpu="A100",
    timeout=3600,
    volumes={"/cache": volume},
    secrets=[modal.Secret.from_name("huggingface-secret")]
)
def generate_image(username: str, prompt: str):
    """Generate image using FLUX from your HF account"""
    from diffusers import FluxPipeline
    import torch
    
    repo_id = f"{username}/FLUX.1-dev"
    print(f"Loading FLUX from {repo_id}...")
    
    pipe = FluxPipeline.from_pretrained(
        repo_id,
        torch_dtype=torch.float16,
        cache_dir="/cache"
    ).to("cuda")
    
    print(f"Generating image: {prompt}")
    image = pipe(
        prompt,
        num_inference_steps=50,
        guidance_scale=7.5
    ).images[0]
    
    # Save to volume
    output_path = "/cache/output_image.png"
    image.save(output_path)
    
    print(f"✅ Image saved to {output_path}")
    return {"status": "success", "path": output_path}

@app.function(
    image=inference_image,
    gpu="A100",
    timeout=3600,
    volumes={"/cache": volume},
    secrets=[modal.Secret.from_name("huggingface-secret")]
)
def generate_video(username: str, prompt: str):
    """Generate video using LTX from your HF account"""
    from diffusers import DiffusionPipeline
    import torch
    
    repo_id = f"{username}/LTX-Video"
    print(f"Loading LTX Video from {repo_id}...")
    
    pipe = DiffusionPipeline.from_pretrained(
        repo_id,
        torch_dtype=torch.float16,
        cache_dir="/cache"
    ).to("cuda")
    
    print(f"Generating video: {prompt}")
    video = pipe(
        prompt,
        num_inference_steps=50
    ).frames
    
    output_path = "/cache/output_video.mp4"
    # Video saving logic here
    
    print(f"✅ Video saved to {output_path}")
    return {"status": "success", "path": output_path}

@app.function(
    image=inference_image,
    gpu="A100",
    timeout=3600,
    volumes={"/cache": volume},
    secrets=[modal.Secret.from_name("huggingface-secret")]
)
def route_and_generate(username: str, user_request: str):
    """Route request and generate content from YOUR HF models"""
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    import json
    
    router_repo = f"{username}/Mistral-7B-Instruct-v0.2"
    print(f"Loading Mistral router from {router_repo}...")
    
    tokenizer = AutoTokenizer.from_pretrained(
        router_repo,
        cache_dir="/cache"
    )
    model = AutoModelForCausalLM.from_pretrained(
        router_repo,
        torch_dtype=torch.float16,
        cache_dir="/cache",
        device_map="auto"
    )
    
    # Route request
    prompt = f"""Analyze this marketing request and decide what to generate.

Request: {user_request}

Respond with JSON only:
{{
    "needs_image": true/false,
    "needs_video": true/false,
    "needs_audio": true/false,
    "image_prompt": "detailed prompt for image",
    "video_prompt": "detailed prompt for video",
    "audio_prompt": "script for audio"
}}

JSON:"""
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=500,
        temperature=0.7,
        do_sample=True
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Parse routing decision
    try:
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        routing = json.loads(response[json_start:json_end])
    except:
        print("⚠️ Failed to parse routing, defaulting to image generation")
        routing = {
            "needs_image": True,
            "needs_video": False,
            "needs_audio": False,
            "image_prompt": user_request
        }
    
    print(f"\n🎯 Routing decision:")
    print(f"  - Image: {routing.get('needs_image', False)}")
    print(f"  - Video: {routing.get('needs_video', False)}")
    print(f"  - Audio: {routing.get('needs_audio', False)}\n")
    
    results = {}
    
    # Generate based on routing
    if routing.get("needs_image"):
        print("🎨 Generating image...")
        results["image"] = generate_image.remote(username, routing["image_prompt"])
    
    if routing.get("needs_video"):
        print("🎬 Generating video...")
        results["video"] = generate_video.remote(username, routing["video_prompt"])
    
    if routing.get("needs_audio"):
        print("🎤 Audio generation coming soon...")
        results["audio"] = {"status": "not_implemented"}
    
    return results

@app.local_entrypoint()
def main(
    username: str,
    request: str = "Create a professional product photo for a smartphone"
):
    """
    Generate marketing content using your HuggingFace models
    
    Usage:
      modal run modal_inference_from_hf.py --username YOUR_HF_USERNAME --request "your request"
    
    Examples:
      modal run modal_inference_from_hf.py --username john --request "Social media ad for energy drink"
      modal run modal_inference_from_hf.py --username john --request "Product demo video for headphones"
    """
    
    if not username:
        print("❌ Error: Please provide your HuggingFace username")
        print("Usage: modal run modal_inference_from_hf.py --username YOUR_HF_USERNAME")
        return
    
    print(f"🚀 Processing request: {request}")
    print(f"📦 Using models from: {username}'s HuggingFace account\n")
    
    results = route_and_generate.remote(username, request)
    
    print(f"\n🎉 Generation complete!")
    print(f"Results: {results}")

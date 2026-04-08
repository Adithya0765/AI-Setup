"""
Modal deployment for inference (no fine-tuning, just generation)
Deploy: modal deploy modal_inference.py
Run: modal run modal_inference.py --request "your marketing request here"
"""

import modal

app = modal.App("marketing-ai-inference")

# Create image with all dependencies
inference_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch",
        "torchvision",
        "diffusers",
        "transformers",
        "accelerate",
        "huggingface_hub",
        "Pillow"
    )
)

# Shared volume for model caching
volume = modal.Volume.from_name("model-cache", create_if_missing=True)

@app.function(
    image=inference_image,
    gpu="A100",
    timeout=3600,
    volumes={"/cache": volume},
    secrets=[modal.Secret.from_name("huggingface-secret")]
)
def generate_image(prompt: str):
    """Generate image using FLUX"""
    from diffusers import FluxPipeline
    import torch
    
    print(f"Loading FLUX model from cache...")
    pipe = FluxPipeline.from_pretrained(
        "/cache/black-forest-labs--FLUX.1-dev",
        torch_dtype=torch.float16,
        local_files_only=True  # Use cached model
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
    
    return {"status": "success", "path": output_path}

@app.function(
    image=inference_image,
    gpu="A100",
    timeout=3600,
    volumes={"/cache": volume},
    secrets=[modal.Secret.from_name("huggingface-secret")]
)
def generate_video(prompt: str):
    """Generate video using LTX"""
    from diffusers import DiffusionPipeline
    import torch
    
    print(f"Loading LTX Video model from cache...")
    pipe = DiffusionPipeline.from_pretrained(
        "/cache/Lightricks--LTX-Video",
        torch_dtype=torch.float16,
        local_files_only=True  # Use cached model
    ).to("cuda")
    
    print(f"Generating video: {prompt}")
    video = pipe(
        prompt,
        num_inference_steps=50
    ).frames
    
    # Save video
    output_path = "/cache/output_video.mp4"
    # Video saving logic here
    
    return {"status": "success", "path": output_path}

@app.function(
    image=inference_image,
    gpu="A100",
    timeout=3600,
    volumes={"/cache": volume},
    secrets=[modal.Secret.from_name("huggingface-secret")]
)
def route_and_generate(user_request: str):
    """Route request and generate appropriate content"""
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    import json
    
    # Load router
    print("Loading Mistral router from cache...")
    tokenizer = AutoTokenizer.from_pretrained(
        "/cache/mistralai--Mistral-7B-Instruct-v0.2",
        local_files_only=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        "/cache/mistralai--Mistral-7B-Instruct-v0.2",
        torch_dtype=torch.float16,
        local_files_only=True,
        device_map="auto"
    )
    
    # Route request
    prompt = f"""Analyze this marketing request and decide what to generate.

Request: {user_request}

Respond with JSON:
{{
    "needs_image": true/false,
    "needs_video": true/false,
    "needs_audio": true/false,
    "image_prompt": "prompt",
    "video_prompt": "prompt",
    "audio_prompt": "script"
}}

JSON:"""
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=500, temperature=0.7)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Parse routing decision
    try:
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        routing = json.loads(response[json_start:json_end])
    except:
        routing = {
            "needs_image": True,
            "needs_video": False,
            "needs_audio": False,
            "image_prompt": user_request
        }
    
    print(f"Routing: {routing}")
    
    results = {}
    
    # Generate based on routing
    if routing.get("needs_image"):
        results["image"] = generate_image.remote(routing["image_prompt"])
    
    if routing.get("needs_video"):
        results["video"] = generate_video.remote(routing["video_prompt"])
    
    return results

@app.local_entrypoint()
def main(request: str = "Create a professional product photo for a smartphone"):
    """Run generation from command line"""
    print(f"Processing request: {request}")
    results = route_and_generate.remote(request)
    print(f"Results: {results}")

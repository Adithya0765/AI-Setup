"""
Marketing AI Router System
Uses Mistral to route requests to appropriate generation models
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from diffusers import FluxPipeline, DiffusionPipeline
import json

class MarketingRouter:
    def __init__(self):
        print("🚀 Loading router (Mistral)...")
        self.router_tokenizer = AutoTokenizer.from_pretrained("./models/mistral-7b")
        self.router_model = AutoModelForCausalLM.from_pretrained(
            "./models/mistral-7b",
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        self.flux_pipe = None
        self.ltx_pipe = None
        self.fish_model = None
        
    def route_request(self, user_request: str):
        """Determine which models to use based on request"""
        
        prompt = f"""You are a marketing AI router. Analyze the request and decide which models to use.

User request: {user_request}

Respond with JSON only:
{{
    "needs_image": true/false,
    "needs_video": true/false,
    "needs_audio": true/false,
    "image_prompt": "detailed prompt for image generation",
    "video_prompt": "detailed prompt for video generation",
    "audio_prompt": "script for voiceover"
}}

JSON:"""

        inputs = self.router_tokenizer(prompt, return_tensors="pt").to(self.router_model.device)
        outputs = self.router_model.generate(
            **inputs,
            max_new_tokens=500,
            temperature=0.7,
            do_sample=True
        )
        
        response = self.router_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract JSON from response
        try:
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            routing_decision = json.loads(response[json_start:json_end])
            return routing_decision
        except:
            print("⚠️ Failed to parse routing decision, using defaults")
            return {
                "needs_image": True,
                "needs_video": False,
                "needs_audio": False,
                "image_prompt": user_request,
                "video_prompt": "",
                "audio_prompt": ""
            }
    
    def load_image_model(self):
        """Load FLUX for image generation"""
        if self.flux_pipe is None:
            print("📸 Loading FLUX image model...")
            self.flux_pipe = FluxPipeline.from_pretrained(
                "./models/flux-dev",
                torch_dtype=torch.float16
            ).to("cuda")
        return self.flux_pipe
    
    def load_video_model(self):
        """Load LTX for video generation"""
        if self.ltx_pipe is None:
            print("🎬 Loading LTX video model...")
            self.ltx_pipe = DiffusionPipeline.from_pretrained(
                "./models/ltx-video",
                torch_dtype=torch.float16
            ).to("cuda")
        return self.ltx_pipe
    
    def load_audio_model(self):
        """Load Fish Speech for audio generation"""
        if self.fish_model is None:
            print("🎤 Loading Fish Speech audio model...")
            # Fish Speech loading logic here
            pass
        return self.fish_model
    
    def generate_content(self, user_request: str):
        """Main function to generate marketing content"""
        
        # Step 1: Route the request
        print(f"\n📋 Request: {user_request}")
        routing = self.route_request(user_request)
        print(f"\n🎯 Routing decision:")
        print(f"  - Image: {routing['needs_image']}")
        print(f"  - Video: {routing['needs_video']}")
        print(f"  - Audio: {routing['needs_audio']}")
        
        results = {}
        
        # Step 2: Generate image if needed
        if routing['needs_image']:
            pipe = self.load_image_model()
            print(f"\n🎨 Generating image: {routing['image_prompt'][:50]}...")
            image = pipe(
                routing['image_prompt'],
                num_inference_steps=50,
                guidance_scale=7.5
            ).images[0]
            image.save("output_image.png")
            results['image'] = "output_image.png"
            print("✅ Image saved to output_image.png")
        
        # Step 3: Generate video if needed
        if routing['needs_video']:
            pipe = self.load_video_model()
            print(f"\n🎬 Generating video: {routing['video_prompt'][:50]}...")
            video = pipe(
                routing['video_prompt'],
                num_inference_steps=50
            ).frames
            # Save video logic here
            results['video'] = "output_video.mp4"
            print("✅ Video saved to output_video.mp4")
        
        # Step 4: Generate audio if needed
        if routing['needs_audio']:
            model = self.load_audio_model()
            print(f"\n🎤 Generating audio: {routing['audio_prompt'][:50]}...")
            # Audio generation logic here
            results['audio'] = "output_audio.wav"
            print("✅ Audio saved to output_audio.wav")
        
        return results

if __name__ == "__main__":
    # Example usage
    router = MarketingRouter()
    
    # Test request
    request = "Create a social media ad for a new smartphone with a professional voiceover"
    results = router.generate_content(request)
    
    print(f"\n🎉 Generated content:")
    for content_type, path in results.items():
        print(f"  - {content_type}: {path}")

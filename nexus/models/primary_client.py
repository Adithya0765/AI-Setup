"""Primary AI client - handles architectural and planning tasks"""

from typing import Dict, Any, List
import aiohttp


class PrimaryClient:
    """Primary AI model for planning and architecture"""
    
    def __init__(self, api_keys: List[str]):
        self.api_keys = api_keys
        self.base_url = "https://openrouter.ai/api/v1"
    
    async def generate(self, prompt: str, api_key: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate response using primary model via OpenRouter"""
        
        full_prompt = prompt
        if context:
            full_prompt = f"Context: {context}\n\n{prompt}"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://nexus.ai",  # Optional, for rankings
            "X-Title": "NEXUS"  # Optional, shows in rankings
        }
        
        # Try models in order of preference
        models = [
            "nvidia/llama-3.1-nemotron-70b-instruct",  # NVIDIA Nemotron 3 Super
            "minimax/minimax-01"  # MiniMax M2.5
        ]
        
        for model in models:
            try:
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "user", "content": full_prompt}
                    ],
                    "temperature": 0.7
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload
                    ) as response:
                        if response.status != 200:
                            # Try next model
                            continue
                        
                        data = await response.json()
                        
                        # Handle response format
                        if "choices" in data and len(data["choices"]) > 0:
                            content = data["choices"][0]["message"]["content"]
                        elif "content" in data:
                            content = data["content"]
                        else:
                            # Try next model
                            continue
                        
                        return {
                            "content": content,
                            "model": "nex1-architect"  # Branded name
                        }
            except Exception:
                # Try next model
                continue
        
        # All models failed
        raise Exception("All primary models unavailable. Please try again.")

"""Secondary AI client - handles fast code execution"""

from typing import Dict, Any, List
import aiohttp


class SecondaryClient:
    """Secondary AI model for fast code generation"""
    
    def __init__(self, api_keys: List[str]):
        self.api_keys = api_keys
        self.base_url = "https://api.x.ai/v1"
    
    async def generate(self, prompt: str, api_key: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate response using secondary model"""
        
        full_prompt = prompt
        if context:
            full_prompt = f"Context: {context}\n\n{prompt}"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {"role": "user", "content": full_prompt}
            ],
            "model": "grok-beta",
            "temperature": 0.7
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Grok API error: {response.status} - {error_text}")
                
                data = await response.json()
                
                # Handle response format
                if "choices" in data and len(data["choices"]) > 0:
                    content = data["choices"][0]["message"]["content"]
                elif "content" in data:
                    content = data["content"]
                else:
                    raise Exception(f"Unexpected Grok API response format: {data}")
                
                return {
                    "content": content,
                    "model": "nex1-builder"  # Branded name
                }

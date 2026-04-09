"""Primary AI client - handles architectural and planning tasks"""

from typing import Dict, Any, List
import google.generativeai as genai


class PrimaryClient:
    """Primary AI model for planning and architecture"""
    
    def __init__(self, api_keys: List[str]):
        self.api_keys = api_keys
    
    async def generate(self, prompt: str, api_key: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate response using primary model"""
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        full_prompt = prompt
        if context:
            full_prompt = f"Context: {context}\n\n{prompt}"
        
        response = model.generate_content(full_prompt)
        
        return {
            "content": response.text,
            "model": "nexus-architect"  # Branded name
        }

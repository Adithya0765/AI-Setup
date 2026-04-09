"""Primary AI client - handles architectural and planning tasks"""

from typing import Dict, Any, List
import warnings

# Suppress the deprecation warning
warnings.filterwarnings('ignore', category=FutureWarning, module='google.generativeai')

try:
    from google import genai
    USE_NEW_API = True
except ImportError:
    import google.generativeai as genai
    USE_NEW_API = False


class PrimaryClient:
    """Primary AI model for planning and architecture"""
    
    def __init__(self, api_keys: List[str]):
        self.api_keys = api_keys
    
    async def generate(self, prompt: str, api_key: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate response using primary model"""
        
        full_prompt = prompt
        if context:
            full_prompt = f"Context: {context}\n\n{prompt}"
        
        if USE_NEW_API:
            # New google.genai API
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=full_prompt
            )
            content = response.text
        else:
            # Old google.generativeai API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(full_prompt)
            content = response.text
        
        return {
            "content": content,
            "model": "nexus-architect"  # Branded name
        }

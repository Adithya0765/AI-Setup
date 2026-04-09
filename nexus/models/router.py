"""Model router with intelligent key rotation and rate limiting"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Literal
from dataclasses import dataclass, field

from nexus.config import Config
from nexus.models.primary_client import PrimaryClient
from nexus.models.secondary_client import SecondaryClient


@dataclass
class KeyState:
    key: str
    requests: int = 0
    cooldown_until: datetime = field(default_factory=datetime.now)
    last_used: datetime = field(default_factory=datetime.now)


class ModelRouter:
    """Intelligent model routing with rate limiting"""
    
    def __init__(self, config: Config):
        self.config = config
        
        # Initialize clients (internal implementation hidden)
        self.primary = PrimaryClient(config.primary_keys)
        self.secondary = SecondaryClient(config.secondary_keys)
        
        # Key management
        self.primary_keys = [KeyState(key=k) for k in config.primary_keys]
        self.secondary_keys = [KeyState(key=k) for k in config.secondary_keys]
        
        self.primary_rpm = config.primary_rpm
        self.secondary_rpm = config.secondary_rpm
    
    async def call(
        self,
        mode: Literal["architect", "builder", "validator"],
        prompt: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Route call to appropriate model with rate limiting
        
        Modes:
        - architect: For planning and high-level design
        - builder: For fast code generation and execution
        - validator: For critical validation (uses both)
        """
        
        if mode == "architect":
            return await self._call_primary(prompt, context)
        elif mode == "builder":
            return await self._call_secondary(prompt, context)
        elif mode == "validator":
            return await self._call_validator(prompt, context)
        else:
            raise ValueError(f"Unknown mode: {mode}")
    
    async def _call_primary(self, prompt: str, context: Dict = None) -> Dict[str, Any]:
        """Call primary model with rate limiting"""
        key = await self._get_available_key(self.primary_keys, self.primary_rpm)
        response = await self.primary.generate(prompt, key.key, context)
        self._update_key_usage(key)
        return response
    
    async def _call_secondary(self, prompt: str, context: Dict = None) -> Dict[str, Any]:
        """Call secondary model with rate limiting"""
        key = await self._get_available_key(self.secondary_keys, self.secondary_rpm)
        response = await self.secondary.generate(prompt, key.key, context)
        self._update_key_usage(key)
        return response
    
    async def _call_validator(self, prompt: str, context: Dict = None) -> Dict[str, Any]:
        """Call both models and merge results for validation"""
        primary_task = self._call_primary(prompt, context)
        secondary_task = self._call_secondary(prompt, context)
        
        primary_result, secondary_result = await asyncio.gather(primary_task, secondary_task)
        
        # Merge results using primary model
        merge_prompt = f"""Merge these two analyses into one coherent validation:

Analysis 1: {secondary_result['content']}

Analysis 2: {primary_result['content']}

Provide a single, refined validation result."""

        return await self._call_primary(merge_prompt, context)
    
    async def _get_available_key(self, keys: List[KeyState], rpm: int) -> KeyState:
        """Get an available key or wait"""
        while True:
            now = datetime.now()
            
            # Find available key
            for key in keys:
                if now >= key.cooldown_until and key.requests < rpm:
                    return key
            
            # Reset keys if minute passed
            for key in keys:
                if (now - key.last_used) >= timedelta(minutes=1):
                    key.requests = 0
                    key.cooldown_until = now
            
            # Wait and retry
            await asyncio.sleep(1)
    
    def _update_key_usage(self, key: KeyState):
        """Update key usage stats"""
        key.requests += 1
        key.last_used = datetime.now()
        
        # Set cooldown if limit reached
        if key.requests >= self.primary_rpm:
            key.cooldown_until = datetime.now() + timedelta(minutes=1)

"""Model router with intelligent key rotation and rate limiting"""

import asyncio
import re
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
    is_rate_limited: bool = False


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
        """Call primary model with rate limiting and key rotation"""
        
        for key in self.primary_keys:
            # Skip rate limited keys
            if key.is_rate_limited and datetime.now() < key.cooldown_until:
                continue
            
            # Reset rate limit flag if cooldown passed
            if key.is_rate_limited and datetime.now() >= key.cooldown_until:
                key.is_rate_limited = False
                key.requests = 0
            
            try:
                response = await self.primary.generate(prompt, key.key, context)
                self._update_key_usage(key, self.primary_rpm)
                return response
            except Exception as e:
                error_msg = str(e)
                
                # Check if it's a rate limit error
                if "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
                    # Extract wait time if available
                    wait_time = self._extract_wait_time(error_msg)
                    
                    # Mark this key as rate limited
                    key.is_rate_limited = True
                    key.cooldown_until = datetime.now() + timedelta(seconds=wait_time)
                    
                    masked_key = f"...{key.key[-4:]}" if len(key.key) > 4 else "****"
                    print(f"[DEBUG] Key {masked_key} rate limited, trying next key...")
                    
                    # Try next key
                    continue
                else:
                    # Other error, raise immediately
                    raise
        
        # All keys are rate limited
        min_wait = min(
            (key.cooldown_until - datetime.now()).total_seconds() 
            for key in self.primary_keys 
            if key.is_rate_limited
        )
        
        raise Exception(f"NEX1 has hit the rate limit. Please wait {int(min_wait)} seconds and try again.")
    
    async def _call_secondary(self, prompt: str, context: Dict = None) -> Dict[str, Any]:
        """Call secondary model with rate limiting and key rotation"""
        
        for key in self.secondary_keys:
            # Skip rate limited keys
            if key.is_rate_limited and datetime.now() < key.cooldown_until:
                continue
            
            # Reset rate limit flag if cooldown passed
            if key.is_rate_limited and datetime.now() >= key.cooldown_until:
                key.is_rate_limited = False
                key.requests = 0
            
            try:
                response = await self.secondary.generate(prompt, key.key, context)
                self._update_key_usage(key, self.secondary_rpm)
                return response
            except Exception as e:
                error_msg = str(e)
                
                # Check if it's a rate limit error
                if "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
                    # Extract wait time if available
                    wait_time = self._extract_wait_time(error_msg)
                    
                    # Mark this key as rate limited
                    key.is_rate_limited = True
                    key.cooldown_until = datetime.now() + timedelta(seconds=wait_time)
                    
                    masked_key = f"...{key.key[-4:]}" if len(key.key) > 4 else "****"
                    print(f"[DEBUG] Key {masked_key} rate limited, trying next key...")
                    
                    # Try next key
                    continue
                else:
                    # Other error, raise immediately
                    raise
        
        # All keys are rate limited
        min_wait = min(
            (key.cooldown_until - datetime.now()).total_seconds() 
            for key in self.secondary_keys 
            if key.is_rate_limited
        )
        
        raise Exception(f"NEX1 has hit the rate limit. Please wait {int(min_wait)} seconds and try again.")
    
    def _extract_wait_time(self, error_msg: str) -> int:
        """Extract wait time from error message"""
        # Try to find "retry in X.Xs" or "wait X seconds"
        match = re.search(r'retry in (\d+\.?\d*)s', error_msg)
        if match:
            return int(float(match.group(1))) + 1  # Add 1 second buffer
        
        match = re.search(r'wait (\d+) seconds', error_msg)
        if match:
            return int(match.group(1)) + 1
        
        # Default to 10 seconds
        return 10
    
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
            
            # Reset keys if minute passed
            for key in keys:
                if (now - key.last_used) >= timedelta(minutes=1):
                    key.requests = 0
                    key.cooldown_until = now
            
            # Find available key (round-robin style)
            for key in keys:
                if now >= key.cooldown_until and key.requests < rpm:
                    # Mask key for logging (show last 4 chars only)
                    masked_key = f"...{key.key[-4:]}" if len(key.key) > 4 else "****"
                    print(f"[DEBUG] Using key {masked_key} ({key.requests}/{rpm} requests)")
                    return key
            
            # All keys exhausted, wait
            print(f"[DEBUG] All keys on cooldown, waiting...")
            await asyncio.sleep(2)
    
    def _update_key_usage(self, key: KeyState, rpm: int):
        """Update key usage stats"""
        key.requests += 1
        key.last_used = datetime.now()
        
        # Set cooldown if limit reached
        if key.requests >= rpm:
            key.cooldown_until = datetime.now() + timedelta(minutes=1)
            key.requests = 0  # Reset for next cycle

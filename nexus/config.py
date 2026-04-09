"""Configuration management"""

import os
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv


class Config(BaseModel):
    # User Authentication
    user_token: Optional[str] = None
    api_endpoint: str = "https://api.nexus.ai/v1"
    
    # Legacy support for self-hosted (optional)
    primary_keys: List[str] = []
    secondary_keys: List[str] = []
    
    # Rate Limits (managed by service)
    primary_rpm: int = 15
    secondary_rpm: int = 60
    
    # Execution
    sandbox_enabled: bool = False
    max_retries: int = 3
    
    # Paths
    memory_dir: Path
    strategy_dir: Path
    workspace_dir: Path


def load_config() -> Config:
    """Load configuration from environment or config file"""
    
    # Try loading from ~/.nexus/config.env first (installed version)
    home_config = Path.home() / ".nexus" / "config.env"
    if home_config.exists():
        load_dotenv(home_config)
    else:
        # Fall back to local .env (development)
        load_dotenv()
    
    workspace = Path.cwd()
    
    # Use home directory for installed version, local for dev
    if home_config.exists():
        nexus_dir = Path.home() / ".nexus"
    else:
        nexus_dir = workspace / ".nexus"
    
    nexus_dir.mkdir(exist_ok=True)
    
    # Load user token (for managed service)
    user_token = os.getenv("NEXUS_USER_TOKEN")
    api_endpoint = os.getenv("NEXUS_API_ENDPOINT", "https://api.nexus.ai/v1")
    
    # Legacy support for self-hosted with own keys
    primary_keys_str = os.getenv("NEXUS_PRIMARY_KEYS", os.getenv("GEMINI_API_KEYS", ""))
    secondary_keys_str = os.getenv("NEXUS_SECONDARY_KEYS", os.getenv("GROK_API_KEYS", ""))
    
    return Config(
        user_token=user_token,
        api_endpoint=api_endpoint,
        primary_keys=[k.strip() for k in primary_keys_str.split(",") if k.strip()],
        secondary_keys=[k.strip() for k in secondary_keys_str.split(",") if k.strip()],
        primary_rpm=int(os.getenv("PRIMARY_RPM", os.getenv("GEMINI_RPM", "15"))),
        secondary_rpm=int(os.getenv("SECONDARY_RPM", os.getenv("GROK_RPM", "60"))),
        sandbox_enabled=os.getenv("ENABLE_SANDBOX", os.getenv("DOCKER_ENABLED", "false")).lower() == "true",
        max_retries=int(os.getenv("MAX_RETRIES", "3")),
        memory_dir=nexus_dir / "memory",
        strategy_dir=nexus_dir / "strategies",
        workspace_dir=workspace
    )

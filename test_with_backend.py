"""Test NEXUS CLI with local backend"""

import asyncio
import os
from nexus.config import load_config
from nexus.orchestrator import Orchestrator

async def test():
    # Set backend URL to local
    os.environ["NEXUS_API_ENDPOINT"] = "http://localhost:8000/api/v1"
    
    # Clear API keys to force backend mode
    os.environ["NEXUS_PRIMARY_KEYS"] = ""
    os.environ["NEXUS_SECONDARY_KEYS"] = ""
    
    print("🧪 Testing NEXUS with local backend...")
    print()
    
    config = load_config()
    print(f"✓ Config loaded")
    print(f"  API Endpoint: {config.api_endpoint}")
    print(f"  Using backend: {not config.primary_keys}")
    print()
    
    orchestrator = Orchestrator(config)
    
    print("📝 Executing task: 'list all Python files'")
    print()
    
    async for update in orchestrator.execute("list all Python files"):
        if update["type"] == "step":
            print(f"  → {update['message']}")
        elif update["type"] == "result":
            print()
            print("✅ Result:")
            print(update["content"])
        elif update["type"] == "error":
            print()
            print("❌ Error:")
            print(update["content"])
        elif update["type"] == "info":
            print(update["content"])

if __name__ == "__main__":
    asyncio.run(test())

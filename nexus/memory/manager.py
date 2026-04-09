"""Memory management system"""

import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime


class MemoryManager:
    def __init__(self, config):
        self.memory_dir = config.memory_dir
        self.memory_dir.mkdir(parents=True, exist_ok=True)
    
    async def store(self, entry: Dict[str, Any]):
        """Store execution memory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"memory_{timestamp}.json"
        
        path = self.memory_dir / filename
        path.write_text(json.dumps(entry, indent=2))
    
    async def retrieve(self, query: str, limit: int = 5) -> List[Dict]:
        """Retrieve relevant memories"""
        # TODO: Implement semantic search
        memories = []
        for file in sorted(self.memory_dir.glob("*.json"), reverse=True)[:limit]:
            memories.append(json.loads(file.read_text()))
        return memories
    
    async def count(self) -> int:
        """Count total memories"""
        return len(list(self.memory_dir.glob("*.json")))
    
    async def success_rate(self) -> float:
        """Calculate success rate"""
        memories = await self.retrieve("", limit=100)
        if not memories:
            return 0.0
        
        successes = sum(1 for m in memories if m.get("evaluation", {}).get("success"))
        return successes / len(memories)

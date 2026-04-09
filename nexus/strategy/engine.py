"""Strategy evolution engine"""

import json
from pathlib import Path
from typing import Dict, List


class StrategyEngine:
    def __init__(self, config):
        self.strategy_dir = config.strategy_dir
        self.strategy_dir.mkdir(parents=True, exist_ok=True)
        self._init_default_strategies()
    
    def _init_default_strategies(self):
        """Initialize default strategies"""
        defaults = [
            {
                "name": "debug_trace",
                "description": "Add logging to trace execution flow",
                "success_rate": 0.7,
                "usage_count": 0
            },
            {
                "name": "test_first",
                "description": "Write tests before implementation",
                "success_rate": 0.8,
                "usage_count": 0
            },
            {
                "name": "incremental_refactor",
                "description": "Refactor in small, testable steps",
                "success_rate": 0.75,
                "usage_count": 0
            }
        ]
        
        for strategy in defaults:
            path = self.strategy_dir / f"{strategy['name']}.json"
            if not path.exists():
                path.write_text(json.dumps(strategy, indent=2))
    
    async def get_relevant(self, task: str, limit: int = 3) -> List[Dict]:
        """Get relevant strategies for task"""
        strategies = []
        for file in self.strategy_dir.glob("*.json"):
            strategy = json.loads(file.read_text())
            strategies.append(strategy)
        
        # Sort by success rate
        strategies.sort(key=lambda s: s["success_rate"], reverse=True)
        return strategies[:limit]
    
    async def update_success(self, strategy_name: str):
        """Update strategy after success"""
        path = self.strategy_dir / f"{strategy_name}.json"
        if path.exists():
            strategy = json.loads(path.read_text())
            strategy["usage_count"] += 1
            strategy["success_rate"] = (
                strategy["success_rate"] * 0.9 + 0.1
            )  # Boost
            path.write_text(json.dumps(strategy, indent=2))
    
    async def update_failure(self, strategy_name: str):
        """Update strategy after failure"""
        path = self.strategy_dir / f"{strategy_name}.json"
        if path.exists():
            strategy = json.loads(path.read_text())
            strategy["usage_count"] += 1
            strategy["success_rate"] = (
                strategy["success_rate"] * 0.9
            )  # Reduce
            path.write_text(json.dumps(strategy, indent=2))
    
    async def count(self) -> int:
        """Count total strategies"""
        return len(list(self.strategy_dir.glob("*.json")))

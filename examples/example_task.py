"""Example: Running NEXUS programmatically"""

import asyncio
from pathlib import Path
from nexus.config import Config
from nexus.orchestrator import Orchestrator


async def main():
    # Setup config
    config = Config(
        gemini_keys=["your-key"],
        grok_keys=["your-key"],
        gemini_rpm=15,
        grok_rpm=60,
        docker_enabled=False,
        max_retries=3,
        memory_dir=Path(".nexus/memory"),
        strategy_dir=Path(".nexus/strategies"),
        workspace_dir=Path.cwd()
    )
    
    # Create orchestrator
    orchestrator = Orchestrator(config)
    
    # Execute task
    task = "analyze the code structure and suggest improvements"
    
    print(f"Executing: {task}\n")
    
    async for update in orchestrator.execute(task):
        if update["type"] == "step":
            print(f"→ {update['message']}")
        elif update["type"] == "result":
            print(f"\n✓ Result:\n{update['content']}")
        elif update["type"] == "error":
            print(f"\n✗ Error:\n{update['content']}")
    
    # Show stats
    stats = await orchestrator.get_stats()
    print(f"\nStats:")
    print(f"  Tasks: {stats['tasks_completed']}")
    print(f"  Success Rate: {stats['success_rate']:.1%}")
    print(f"  Strategies: {stats['strategies_count']}")


if __name__ == "__main__":
    asyncio.run(main())

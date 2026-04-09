#!/usr/bin/env python3
"""
Quick test to verify NEXUS CLI is working
"""

import asyncio
from pathlib import Path
from rich.console import Console

console = Console()

async def test_imports():
    """Test that all imports work"""
    console.print("\n[bold]Testing imports...[/bold]")
    
    try:
        from nexus.config import load_config
        console.print("✓ Config module")
        
        from nexus.orchestrator import Orchestrator
        console.print("✓ Orchestrator module")
        
        from nexus.cli import CLI
        console.print("✓ CLI module")
        
        from nexus.models.router import ModelRouter
        console.print("✓ Model router")
        
        from nexus.agents.planner import Planner
        console.print("✓ Planner agent")
        
        from nexus.agents.executor import Executor
        console.print("✓ Executor agent")
        
        from nexus.agents.evaluator import Evaluator
        console.print("✓ Evaluator agent")
        
        from nexus.memory.manager import MemoryManager
        console.print("✓ Memory manager")
        
        from nexus.strategy.engine import StrategyEngine
        console.print("✓ Strategy engine")
        
        return True
    except Exception as e:
        console.print(f"[red]✗ Import failed: {e}[/red]")
        return False


async def test_config():
    """Test configuration loading"""
    console.print("\n[bold]Testing configuration...[/bold]")
    
    try:
        from nexus.config import load_config
        config = load_config()
        
        console.print(f"✓ Config loaded")
        console.print(f"  Workspace: {config.workspace_dir}")
        console.print(f"  Memory dir: {config.memory_dir}")
        console.print(f"  Strategy dir: {config.strategy_dir}")
        
        return True
    except Exception as e:
        console.print(f"[red]✗ Config failed: {e}[/red]")
        return False


async def test_orchestrator():
    """Test orchestrator initialization"""
    console.print("\n[bold]Testing orchestrator...[/bold]")
    
    try:
        from nexus.config import load_config
        from nexus.orchestrator import Orchestrator
        
        config = load_config()
        orchestrator = Orchestrator(config)
        
        console.print("✓ Orchestrator created")
        
        # Get stats
        stats = await orchestrator.get_stats()
        console.print(f"✓ Stats retrieved:")
        console.print(f"  Tasks completed: {stats['tasks_completed']}")
        console.print(f"  Success rate: {stats['success_rate']:.1%}")
        console.print(f"  Strategies: {stats['strategies_count']}")
        console.print(f"  Memory entries: {stats['memory_entries']}")
        
        return True
    except Exception as e:
        console.print(f"[red]✗ Orchestrator failed: {e}[/red]")
        import traceback
        traceback.print_exc()
        return False


async def test_strategies():
    """Test strategy engine"""
    console.print("\n[bold]Testing strategy engine...[/bold]")
    
    try:
        from nexus.config import load_config
        from nexus.strategy.engine import StrategyEngine
        
        config = load_config()
        engine = StrategyEngine(config)
        
        strategies = await engine.get_relevant("test task", limit=3)
        console.print(f"✓ Found {len(strategies)} strategies:")
        
        for s in strategies:
            console.print(f"  • {s['name']}: {s['success_rate']:.1%} success rate")
        
        return True
    except Exception as e:
        console.print(f"[red]✗ Strategy engine failed: {e}[/red]")
        return False


async def test_memory():
    """Test memory system"""
    console.print("\n[bold]Testing memory system...[/bold]")
    
    try:
        from nexus.config import load_config
        from nexus.memory.manager import MemoryManager
        
        config = load_config()
        memory = MemoryManager(config)
        
        count = await memory.count()
        console.print(f"✓ Memory entries: {count}")
        
        if count > 0:
            rate = await memory.success_rate()
            console.print(f"✓ Success rate: {rate:.1%}")
        
        return True
    except Exception as e:
        console.print(f"[red]✗ Memory system failed: {e}[/red]")
        return False


async def main():
    """Run all tests"""
    console.print("\n╔═══════════════════════════════════════════════════════════╗")
    console.print("║                                                           ║")
    console.print("║   [bold cyan]NEXUS CLI Test Suite[/bold cyan]                                 ║")
    console.print("║                                                           ║")
    console.print("╚═══════════════════════════════════════════════════════════╝")
    
    results = []
    
    # Run tests
    results.append(("Imports", await test_imports()))
    results.append(("Configuration", await test_config()))
    results.append(("Orchestrator", await test_orchestrator()))
    results.append(("Strategies", await test_strategies()))
    results.append(("Memory", await test_memory()))
    
    # Summary
    console.print("\n[bold]Test Summary:[/bold]")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[green]✓ PASS[/green]" if result else "[red]✗ FAIL[/red]"
        console.print(f"  {status} {name}")
    
    console.print(f"\n[bold]Results: {passed}/{total} tests passed[/bold]")
    
    if passed == total:
        console.print("\n[bold green]✓ All tests passed! CLI is working correctly.[/bold green]")
        console.print("\n[dim]Next: Run 'python demo.py' to see the user experience[/dim]")
    else:
        console.print("\n[bold red]✗ Some tests failed. Check the errors above.[/bold red]")
        console.print("\n[dim]Make sure you've installed dependencies: pip install -r requirements.txt[/dim]")
    
    console.print()


if __name__ == "__main__":
    asyncio.run(main())

"""CLI entry point for NEXUS"""

import sys
import asyncio
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from nexus.cli import CLI
from nexus.config import load_config

console = Console()


async def main():
    if len(sys.argv) < 2:
        console.print(Panel(
            "[bold cyan]NEXUS[/bold cyan] - Self-Evolving Coding Intelligence\n\n"
            "Usage:\n"
            "  nexus \"<task description>\"\n"
            "  nexus --interactive\n"
            "  nexus --status\n\n"
            "Examples:\n"
            "  nexus \"fix the auth bug in login.py\"\n"
            "  nexus \"add logging to all error handlers\"\n"
            "  nexus \"refactor the payment module\"",
            title="NEXUS",
            border_style="cyan"
        ))
        return

    try:
        config = load_config()
        cli = CLI(config)
        
        if sys.argv[1] == "--interactive":
            await cli.interactive_mode()
        elif sys.argv[1] == "--status":
            await cli.show_status()
        else:
            task = " ".join(sys.argv[1:])
            await cli.execute_task(task)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise


if __name__ == "__main__":
    asyncio.run(main())

"""CLI entry point for NEXUS"""

import sys
import asyncio
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from nexus.cli import CLI
from nexus.config import load_config

console = Console()


def show_welcome():
    """Show cool ASCII art welcome screen"""
    
    # ASCII art logo
    logo = """
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
    """
    
    # Print logo
    console.print(logo, style="bold cyan")
    console.print("    Self-Evolving AI Coding Intelligence", style="dim cyan")
    console.print()
    
    # Welcome message
    console.print("    [bold white]Welcome back![/bold white]")
    console.print()
    
    # Tips section
    console.print("    [bold yellow]Tips for getting started[/bold yellow]")
    console.print("    [dim]Run /init to create a NEXUS.md file with instructions for NEXUS[/dim]")
    console.print("    [dim]Note: You have launched NEXUS in your home directory. For the best experience,[/dim]")
    console.print("    [dim]      launch it in a project directory instead.[/dim]")
    console.print()
    
    # Recent activity
    console.print("    [bold yellow]Recent activity[/bold yellow]")
    console.print("    [dim]No recent activity[/dim]")
    console.print()
    
    # Usage section
    console.print("    [bold yellow]Usage[/bold yellow]")
    console.print("    [cyan]nexus[/cyan] [dim]\"<task description>\"[/dim]     Execute a coding task")
    console.print("    [cyan]nexus --interactive[/cyan]              Start interactive mode")
    console.print("    [cyan]nexus --status[/cyan]                   Show system status")
    console.print()
    
    # Examples
    console.print("    [bold yellow]Examples[/bold yellow]")
    console.print("    [cyan]nexus[/cyan] [dim]\"fix the auth bug in login.py\"[/dim]")
    console.print("    [cyan]nexus[/cyan] [dim]\"add logging to all error handlers\"[/dim]")
    console.print("    [cyan]nexus[/cyan] [dim]\"refactor the payment module\"[/dim]")
    console.print()
    
    # Footer
    console.print("    [dim]● high   ● /effort[/dim]")
    console.print()


async def main():
    # If no arguments, start interactive mode by default (like Claude Code)
    if len(sys.argv) < 2:
        show_welcome()
        
        # Start interactive mode automatically
        try:
            config = load_config()
            cli = CLI(config)
            await cli.interactive_mode()
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        return

    try:
        config = load_config()
        cli = CLI(config)
        
        if sys.argv[1] == "--interactive":
            await cli.interactive_mode()
        elif sys.argv[1] == "--status":
            await cli.show_status()
        elif sys.argv[1] == "--help":
            show_welcome()
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

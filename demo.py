#!/usr/bin/env python3
"""
NEXUS CLI Demo - Shows what the user experience looks like
Run this to see NEXUS in action (without needing API keys)
"""

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import time
import sys

console = Console()

def demo_single_task():
    """Demo a single task execution"""
    console.print("\n[bold cyan]Demo: Single Task Execution[/bold cyan]\n")
    
    # Show command
    console.print("[dim]$ nexus \"fix the authentication bug in auth.py\"[/dim]\n")
    
    # Show startup
    console.print(Panel(
        "[bold]Task:[/bold] fix the authentication bug in auth.py",
        title="NEXUS Starting",
        border_style="cyan"
    ))
    
    # Show progress
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Analyzing...", total=None)
        
        steps = [
            ("Analyzing code...", 1.5),
            ("Planning approach...", 1.0),
            ("Executing changes...", 2.0),
            ("Validating results...", 1.0)
        ]
        
        for step, duration in steps:
            progress.update(task, description=step)
            time.sleep(duration)
            console.print(f"  → {step}")
    
    # Show result
    console.print("\n")
    console.print(Panel(
        "[green]✓ Bug fixed successfully[/green]\n\n"
        "Changes made:\n"
        "• Updated token validation logic\n"
        "• Added proper error handling\n"
        "• Improved session management\n"
        "• Added timeout configuration",
        title="Result",
        border_style="green"
    ))
    
    console.print("\n[dim]Free prompts remaining: 4/5[/dim]")
    console.print("[dim]Want more? Run: nexus --signup[/dim]")


def demo_interactive():
    """Demo interactive mode"""
    console.print("\n\n[bold cyan]Demo: Interactive Mode[/bold cyan]\n")
    
    console.print("[dim]$ nexus --interactive[/dim]\n")
    
    console.print("[bold cyan]NEXUS Interactive Mode[/bold cyan]")
    console.print("Type 'exit' to quit\n")
    
    # Simulate some commands
    commands = [
        ("analyze the codebase structure", "Found 42 Python files, 15 modules, 3 main components"),
        ("find all TODO comments", "Found 7 TODO items across 5 files"),
        ("list security issues", "No critical security issues found. 2 minor warnings."),
    ]
    
    for cmd, result in commands:
        console.print(f"[bold green]nexus>[/bold green] {cmd}")
        time.sleep(0.5)
        console.print(f"[dim]Executing...[/dim]")
        time.sleep(1)
        console.print(f"✓ {result}\n")
    
    console.print("[bold green]nexus>[/bold green] exit")
    console.print("[yellow]Goodbye![/yellow]")


def demo_status():
    """Demo status command"""
    console.print("\n\n[bold cyan]Demo: Status Check[/bold cyan]\n")
    
    console.print("[dim]$ nexus --status[/dim]\n")
    
    console.print(Panel(
        "[bold]Account:[/bold] Free Tier\n"
        "[bold]Prompts Used:[/bold] 5/50 this month\n"
        "[bold]Success Rate:[/bold] 87%\n"
        "[bold]Strategies Learned:[/bold] 15\n"
        "[bold]Tasks Completed:[/bold] 42",
        title="NEXUS Status",
        border_style="cyan"
    ))


def demo_upgrade():
    """Demo upgrade flow"""
    console.print("\n\n[bold cyan]Demo: Upgrade to Pro[/bold cyan]\n")
    
    console.print("[dim]$ nexus --upgrade[/dim]\n")
    
    console.print(Panel(
        "[bold]Current Plan:[/bold] Free (5/50 prompts used)\n\n"
        "[bold cyan]Upgrade to Pro?[/bold cyan]\n"
        "✓ Unlimited prompts\n"
        "✓ Priority support\n"
        "✓ Advanced features\n"
        "✓ Faster execution\n\n"
        "[bold]$29/month[/bold]",
        title="Upgrade",
        border_style="yellow"
    ))
    
    console.print("\n[dim]Visit: https://nexus.ai/upgrade[/dim]")


def demo_limit_reached():
    """Demo when free prompts are exhausted"""
    console.print("\n\n[bold cyan]Demo: Free Prompts Exhausted[/bold cyan]\n")
    
    console.print("[dim]$ nexus \"another task\"[/dim]\n")
    
    console.print(Panel(
        "[yellow]⚠️  Free prompts used (5/5)[/yellow]\n\n"
        "Create a free account for 50 prompts/month:\n"
        "  [bold]nexus --signup[/bold]\n\n"
        "Or upgrade to Pro for unlimited:\n"
        "  [bold]nexus --upgrade[/bold]",
        title="Limit Reached",
        border_style="yellow"
    ))


def main():
    """Run all demos"""
    console.print("\n")
    console.print("╔═══════════════════════════════════════════════════════════╗")
    console.print("║                                                           ║")
    console.print("║   [bold cyan]NEXUS - Self-Evolving Coding Intelligence[/bold cyan]          ║")
    console.print("║                                                           ║")
    console.print("║   [dim]This demo shows what users will experience[/dim]            ║")
    console.print("║                                                           ║")
    console.print("╚═══════════════════════════════════════════════════════════╝")
    
    try:
        # Run demos
        demo_single_task()
        time.sleep(2)
        
        demo_interactive()
        time.sleep(2)
        
        demo_status()
        time.sleep(2)
        
        demo_upgrade()
        time.sleep(2)
        
        demo_limit_reached()
        
        # Final message
        console.print("\n\n")
        console.print("╔═══════════════════════════════════════════════════════════╗")
        console.print("║                                                           ║")
        console.print("║   [bold green]✓ Demo Complete![/bold green]                                    ║")
        console.print("║                                                           ║")
        console.print("║   This is what NEXUS will look like for users.           ║")
        console.print("║                                                           ║")
        console.print("║   [bold]Next steps:[/bold]                                          ║")
        console.print("║   1. Build the backend (GETTING_STARTED.md)              ║")
        console.print("║   2. Connect CLI to backend                              ║")
        console.print("║   3. Test with real AI                                   ║")
        console.print("║                                                           ║")
        console.print("╚═══════════════════════════════════════════════════════════╝")
        console.print("\n")
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted[/yellow]")
        sys.exit(0)


if __name__ == "__main__":
    main()

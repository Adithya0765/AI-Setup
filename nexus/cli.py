"""CLI interface for NEXUS"""

import asyncio
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from nexus.config import Config
from nexus.orchestrator import Orchestrator


class CLI:
    def __init__(self, config: Config):
        self.config = config
        self.console = Console()
        self.orchestrator = Orchestrator(config)
    
    async def execute_task(self, task: str):
        """Execute a single task"""
        self.console.print(Panel(
            f"[bold]Task:[/bold] {task}",
            title="NEXUS Starting",
            border_style="cyan"
        ))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task_id = progress.add_task("Analyzing...", total=None)
            
            async for update in self.orchestrator.execute(task):
                progress.update(task_id, description=update["message"])
                
                if update["type"] == "step":
                    self.console.print(f"  → {update['message']}")
                elif update["type"] == "result":
                    self.console.print(Panel(
                        update["content"],
                        title="Result",
                        border_style="green"
                    ))
                elif update["type"] == "error":
                    self.console.print(Panel(
                        update["content"],
                        title="Error",
                        border_style="red"
                    ))
    
    async def interactive_mode(self):
        """Interactive REPL mode"""
        self.console.print("[bold cyan]NEXUS Interactive Mode[/bold cyan]")
        self.console.print("Type 'exit' to quit\n")
        
        while True:
            try:
                task = self.console.input("[bold green]nexus>[/bold green] ")
                if task.lower() in ["exit", "quit"]:
                    break
                if task.strip():
                    await self.execute_task(task)
            except EOFError:
                break
    
    async def show_status(self):
        """Show system status"""
        stats = await self.orchestrator.get_stats()
        
        self.console.print(Panel(
            f"[bold]Tasks Completed:[/bold] {stats['tasks_completed']}\n"
            f"[bold]Success Rate:[/bold] {stats['success_rate']:.1%}\n"
            f"[bold]Strategies Learned:[/bold] {stats['strategies_count']}\n"
            f"[bold]Memory Entries:[/bold] {stats['memory_entries']}",
            title="NEXUS Status",
            border_style="cyan"
        ))

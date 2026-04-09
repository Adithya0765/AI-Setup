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
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task_id = progress.add_task("Working...", total=None)
            
            async for update in self.orchestrator.execute(task):
                if update["type"] == "step":
                    progress.update(task_id, description=update['message'])
                elif update["type"] == "result":
                    progress.stop()
                    self.console.print(f"\n{update['content']}")
                elif update["type"] == "error":
                    progress.stop()
                    self.console.print(f"\n[red]Error:[/red] {update['content']}")
                elif update["type"] == "info":
                    progress.stop()
                    self.console.print(f"[dim]{update['content']}[/dim]")
    
    async def interactive_mode(self):
        """Interactive REPL mode - like Claude Code"""
        
        while True:
            try:
                task = self.console.input("\n[bold cyan]nexus>[/bold cyan] ")
                
                if task.lower() in ["exit", "quit", "/exit", "/quit"]:
                    self.console.print("\n[yellow]Goodbye![/yellow]")
                    break
                
                if not task.strip():
                    continue
                
                # Execute the task
                await self.execute_task(task)
                
            except EOFError:
                self.console.print("\n[yellow]Goodbye![/yellow]")
                break
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Use 'exit' to quit[/yellow]")
                continue
    
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

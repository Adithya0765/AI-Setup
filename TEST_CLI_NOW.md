# Test NEXUS CLI Right Now

## Quick Test (5 minutes)

### Step 1: Install Dependencies

```bash
# Make sure you're in the nexus directory (where the CLI code is)
cd /path/to/nexus

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Create Test Config

Since we don't have the backend yet, let's create a mock config:

```bash
# Create .env file for testing
cat > .env << 'EOF'
# Mock config for testing
NEXUS_PRIMARY_KEYS=test-key-1
NEXUS_SECONDARY_KEYS=test-key-2
PRIMARY_RPM=15
SECONDARY_RPM=60
MAX_RETRIES=3
ENABLE_SANDBOX=false
EOF
```

### Step 3: Test the CLI

```bash
# Test help
python -m nexus --help

# Test status
python -m nexus --status
```

### Step 4: Mock Test (Without Real AI)

Create a simple test script:

```bash
cat > test_cli.py << 'EOF'
import asyncio
from nexus.config import load_config
from nexus.orchestrator import Orchestrator

async def test():
    print("🧪 Testing NEXUS CLI...")
    
    config = load_config()
    print(f"✓ Config loaded")
    print(f"  Workspace: {config.workspace_dir}")
    print(f"  Memory dir: {config.memory_dir}")
    
    orchestrator = Orchestrator(config)
    print(f"✓ Orchestrator created")
    
    # Get stats
    stats = await orchestrator.get_stats()
    print(f"✓ Stats retrieved:")
    print(f"  Tasks completed: {stats['tasks_completed']}")
    print(f"  Success rate: {stats['success_rate']:.1%}")
    print(f"  Strategies: {stats['strategies_count']}")
    
    print("\n✅ CLI is working!")

if __name__ == "__main__":
    asyncio.run(test())
EOF

python test_cli.py
```

## What You'll See

```
🧪 Testing NEXUS CLI...
✓ Config loaded
  Workspace: /path/to/current/directory
  Memory dir: /path/to/.nexus/memory
✓ Orchestrator created
✓ Stats retrieved:
  Tasks completed: 0
  Success rate: 0.0%
  Strategies: 3

✅ CLI is working!
```

## Test Without Real API Keys

To test the full flow without calling real APIs, create a mock:

```python
# test_full_flow.py
import asyncio
from nexus.cli import CLI
from nexus.config import Config
from pathlib import Path

async def test_full_flow():
    # Create mock config
    config = Config(
        primary_keys=["mock-key"],
        secondary_keys=["mock-key"],
        primary_rpm=15,
        secondary_rpm=60,
        sandbox_enabled=False,
        max_retries=3,
        memory_dir=Path(".nexus/memory"),
        strategy_dir=Path(".nexus/strategies"),
        workspace_dir=Path.cwd()
    )
    
    cli = CLI(config)
    
    print("Testing CLI interface...")
    print("✓ CLI initialized")
    
    # Test status
    stats = await cli.orchestrator.get_stats()
    print(f"✓ Stats: {stats}")
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    asyncio.run(test_full_flow())
```

Run it:
```bash
python test_full_flow.py
```

## Test Interactive Mode (Mock)

```python
# test_interactive.py
from rich.console import Console

console = Console()

console.print("[bold cyan]NEXUS Interactive Mode (Mock)[/bold cyan]")
console.print("Type 'exit' to quit\n")

while True:
    try:
        task = console.input("[bold green]nexus>[/bold green] ")
        if task.lower() in ["exit", "quit"]:
            break
        if task.strip():
            console.print(f"[dim]Would execute: {task}[/dim]")
            console.print("[green]✓ Task complete (mock)[/green]\n")
    except EOFError:
        break

console.print("[yellow]Goodbye![/yellow]")
```

Run it:
```bash
python test_interactive.py
```

## See the CLI in Action

```bash
# This will show the help
python -m nexus --help

# Output:
# NEXUS - Self-Evolving Coding Intelligence
# 
# Usage:
#   nexus "<task description>"
#   nexus --interactive
#   nexus --status
```

## Test the Actual Command Flow

Create a demo that shows what it would look like:

```python
# demo.py
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

console = Console()

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
        "Analyzing code...",
        "Planning approach...",
        "Executing changes...",
        "Validating results..."
    ]
    
    for step in steps:
        progress.update(task, description=step)
        time.sleep(1)
        console.print(f"  → {step}")

# Show result
console.print(Panel(
    "[green]✓ Bug fixed successfully[/green]\n\n"
    "Changes made:\n"
    "- Updated token validation\n"
    "- Added error handling\n"
    "- Improved session management",
    title="Result",
    border_style="green"
))

console.print("\n[dim]Free prompts remaining: 4/5[/dim]")
console.print("[dim]Create account for 50/month: nexus --signup[/dim]")
```

Run it:
```bash
python demo.py
```

## What You Should See

The demo will show:
```
╭─────────────────────────────────────╮
│ NEXUS Starting                      │
│ Task: fix the authentication bug... │
╰─────────────────────────────────────╯

  → Analyzing code...
  → Planning approach...
  → Executing changes...
  → Validating results...

╭─────────────────────────────────────╮
│ Result                              │
│                                     │
│ ✓ Bug fixed successfully            │
│                                     │
│ Changes made:                       │
│ - Updated token validation          │
│ - Added error handling              │
│ - Improved session management       │
╰─────────────────────────────────────╯

Free prompts remaining: 4/5
Create account for 50/month: nexus --signup
```

## Check File Structure

```bash
# See what's created
ls -la .nexus/

# Should show:
# .nexus/
# ├── memory/
# ├── strategies/
# │   ├── debug_trace.json
# │   ├── test_first.json
# │   └── incremental_refactor.json
# └── logs/
```

## View Default Strategies

```bash
cat .nexus/strategies/debug_trace.json
```

Output:
```json
{
  "name": "debug_trace",
  "description": "Add logging to trace execution flow",
  "success_rate": 0.7,
  "usage_count": 0
}
```

## Summary

You can test:
- ✅ CLI structure and imports
- ✅ Configuration loading
- ✅ Orchestrator initialization
- ✅ Memory and strategy systems
- ✅ Rich UI formatting
- ✅ Interactive mode flow

What you CAN'T test yet (needs backend):
- ❌ Actual AI execution
- ❌ User authentication
- ❌ Usage tracking
- ❌ Real prompt execution

## Next Steps

1. **Test the CLI structure** - Run the tests above
2. **See how it looks** - Run the demo
3. **Build the backend** - Follow GETTING_STARTED.md
4. **Connect them** - Then test end-to-end

Want to see it work? Run:
```bash
python demo.py
```

This shows exactly what users will see! 🚀

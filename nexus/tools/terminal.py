"""Terminal execution tool"""

import asyncio
from pathlib import Path


class Terminal:
    def __init__(self, workspace: Path):
        self.workspace = workspace
    
    async def run(self, command: str, timeout: int = 30) -> str:
        """Run shell command"""
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.workspace
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            
            output = stdout.decode() + stderr.decode()
            return output
        
        except asyncio.TimeoutError:
            process.kill()
            return f"Command timed out after {timeout}s"

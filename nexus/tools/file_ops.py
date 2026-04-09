"""File operations tool"""

from pathlib import Path
from typing import Union


class FileOps:
    def __init__(self, workspace: Path):
        self.workspace = workspace
    
    async def read(self, path: Union[str, Path]) -> str:
        """Read file content"""
        full_path = self.workspace / path
        return full_path.read_text()
    
    async def write(self, path: Union[str, Path], content: str):
        """Write file content"""
        full_path = self.workspace / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
    
    async def exists(self, path: Union[str, Path]) -> bool:
        """Check if file exists"""
        full_path = self.workspace / path
        return full_path.exists()
    
    async def list_files(self, pattern: str = "**/*.py") -> list:
        """List files matching pattern"""
        return list(self.workspace.glob(pattern))

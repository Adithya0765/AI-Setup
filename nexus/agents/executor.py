"""Executor agent - performs actions"""

from typing import Dict, Any
from pathlib import Path

from nexus.tools.file_ops import FileOps
from nexus.tools.terminal import Terminal


class Executor:
    def __init__(self, router, config):
        self.router = router
        self.config = config
        self.file_ops = FileOps(config.workspace_dir)
        self.terminal = Terminal(config.workspace_dir)
    
    async def execute_step(self, step: Dict, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step"""
        
        action = step["action"]
        target = step.get("target", "")
        
        try:
            if action == "read_file":
                content = await self.file_ops.read(target)
                return {"success": True, "content": content}
            
            elif action == "write_file":
                # Generate code using builder model
                prompt = f"""Generate code for this task:
{step['description']}

File: {target}
Context: {context}

Return ONLY the code, no explanations."""
                
                response = await self.router.call("builder", prompt, context)
                code = response["content"]
                
                await self.file_ops.write(target, code)
                return {"success": True, "content": code}
            
            elif action == "run_command":
                output = await self.terminal.run(target)
                return {"success": True, "output": output}
            
            elif action == "analyze_code":
                content = await self.file_ops.read(target)
                
                prompt = f"""Analyze this code:

{content}

Task: {step['description']}

Provide analysis."""
                
                response = await self.router.call("architect", prompt, context)
                return {"success": True, "analysis": response["content"]}
            
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}

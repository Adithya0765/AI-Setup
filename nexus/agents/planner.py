"""Planner agent - creates execution plans"""

import json
from typing import Dict, Any, List


class Planner:
    def __init__(self, router):
        self.router = router
    
    async def create_plan(
        self,
        task: str,
        context: Dict[str, Any],
        strategies: List[Dict] = None
    ) -> Dict[str, Any]:
        """Create execution plan for task"""
        
        strategy_context = ""
        if strategies:
            strategy_context = "\n\nRelevant past strategies:\n" + "\n".join(
                f"- {s['name']}: {s['description']} (success rate: {s['success_rate']:.1%})"
                for s in strategies
            )
        
        prompt = f"""Analyze this coding task and create a step-by-step execution plan.

Task: {task}

Workspace: {context.get('workspace', 'unknown')}
{strategy_context}

Return a JSON plan with this structure:
{{
    "analysis": "brief analysis of the task",
    "strategy_used": "name of strategy to use",
    "steps": [
        {{
            "description": "what to do",
            "action": "read_file|write_file|run_command|analyze_code",
            "target": "file or command",
            "reasoning": "why this step"
        }}
    ]
}}"""

        response = await self.router.call("architect", prompt, context)
        
        # Parse JSON from response
        content = response["content"]
        start = content.find("{")
        end = content.rfind("}") + 1
        plan_json = json.loads(content[start:end])
        
        return plan_json
    
    async def refine_step(self, step: Dict, evaluation: Dict) -> Dict:
        """Refine a failed step"""
        
        prompt = f"""This step failed. Refine it to fix the issue.

Original step: {json.dumps(step, indent=2)}

Failure reason: {evaluation['reason']}

Return a refined step in the same JSON format."""

        response = await self.router.call("architect", prompt)
        content = response["content"]
        start = content.find("{")
        end = content.rfind("}") + 1
        
        return json.loads(content[start:end])

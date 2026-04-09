"""Evaluator agent - checks correctness"""

import json
from typing import Dict, Any, List


class Evaluator:
    def __init__(self, router):
        self.router = router
    
    async def evaluate(self, step: Dict, result: Dict) -> Dict[str, Any]:
        """Evaluate a single step result"""
        
        if not result.get("success"):
            return {
                "success": False,
                "reason": result.get("error", "Unknown error")
            }
        
        prompt = f"""Evaluate if this step was successful:

Step: {step['description']}
Action: {step['action']}
Result: {json.dumps(result, indent=2)}

Return JSON:
{{
    "success": true/false,
    "reason": "explanation",
    "confidence": 0.0-1.0
}}"""

        response = await self.router.call("architect", prompt)
        content = response["content"]
        start = content.find("{")
        end = content.rfind("}") + 1
        
        return json.loads(content[start:end])
    
    async def evaluate_final(self, task: str, results: List[Dict]) -> Dict[str, Any]:
        """Evaluate overall task completion"""
        
        prompt = f"""Evaluate if this task was completed successfully:

Task: {task}

Results: {json.dumps(results, indent=2)}

Return JSON:
{{
    "success": true/false,
    "summary": "what was accomplished",
    "issues": ["any problems"],
    "confidence": 0.0-1.0
}}"""

        response = await self.router.call("validator", prompt)
        content = response["content"]
        start = content.find("{")
        end = content.rfind("}") + 1
        
        return json.loads(content[start:end])

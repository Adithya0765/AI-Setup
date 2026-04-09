"""Central orchestrator - the brain of NEXUS"""

import asyncio
from typing import AsyncGenerator, Dict, Any
from datetime import datetime

from nexus.config import Config
from nexus.models.router import ModelRouter
from nexus.agents.planner import Planner
from nexus.agents.executor import Executor
from nexus.agents.evaluator import Evaluator
from nexus.memory.manager import MemoryManager
from nexus.strategy.engine import StrategyEngine


class Orchestrator:
    """Central brain that coordinates all components"""
    
    def __init__(self, config: Config):
        self.config = config
        self.router = ModelRouter(config)
        self.planner = Planner(self.router)
        self.executor = Executor(self.router, config)
        self.evaluator = Evaluator(self.router)
        self.memory = MemoryManager(config)
        self.strategy = StrategyEngine(config)
    
    async def execute(self, task: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Main agent loop"""
        
        start_time = datetime.now()
        
        try:
            # Step 1: Retrieve context
            yield {"type": "step", "message": "Retrieving repo context..."}
            context = await self._get_context(task)
            
            # Step 2: Get relevant strategies
            strategies = await self.strategy.get_relevant(task)
            
            # Step 3: Plan
            yield {"type": "step", "message": "Planning approach..."}
            plan = await self.planner.create_plan(task, context, strategies)
            
            # Step 4: Execute steps
            results = []
            for i, step in enumerate(plan["steps"], 1):
                yield {"type": "step", "message": f"Step {i}/{len(plan['steps'])}: {step['description']}"}
                
                result = await self.executor.execute_step(step, context)
                results.append(result)
                
                # Evaluate after each step
                evaluation = await self.evaluator.evaluate(step, result)
                
                if not evaluation["success"]:
                    # Retry with refinement
                    yield {"type": "step", "message": f"Refining step {i}..."}
                    refined_step = await self.planner.refine_step(step, evaluation)
                    result = await self.executor.execute_step(refined_step, context)
                    results[-1] = result
            
            # Step 5: Final evaluation
            yield {"type": "step", "message": "Evaluating results..."}
            final_eval = await self.evaluator.evaluate_final(task, results)
            
            # Step 6: Store learning
            await self._store_learning(task, plan, results, final_eval)
            
            # Step 7: Return result
            yield {
                "type": "result",
                "content": final_eval["summary"],
                "success": final_eval["success"]
            }
            
        except Exception as e:
            yield {
                "type": "error",
                "content": str(e)
            }
    
    async def _get_context(self, task: str) -> Dict[str, Any]:
        """Retrieve relevant repo context"""
        # TODO: Implement RAG system
        return {
            "workspace": str(self.config.workspace_dir),
            "files": []
        }
    
    async def _store_learning(self, task: str, plan: Dict, results: list, evaluation: Dict):
        """Store execution for learning"""
        await self.memory.store({
            "task": task,
            "plan": plan,
            "results": results,
            "evaluation": evaluation,
            "timestamp": datetime.now().isoformat()
        })
        
        if evaluation["success"]:
            await self.strategy.update_success(plan["strategy_used"])
        else:
            await self.strategy.update_failure(plan["strategy_used"])
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            "tasks_completed": await self.memory.count(),
            "success_rate": await self.memory.success_rate(),
            "strategies_count": await self.strategy.count(),
            "memory_entries": await self.memory.count()
        }

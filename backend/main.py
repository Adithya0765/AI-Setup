"""NEXUS Backend API - Minimal version for testing"""

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# Load your API keys from .env (on server only, never in git)
load_dotenv()

app = FastAPI(title="NEXUS API")

class TaskRequest(BaseModel):
    task: str
    context: Optional[dict] = None

class TaskResponse(BaseModel):
    success: bool
    result: str
    prompts_remaining: int

# Mock user database (replace with real DB later)
MOCK_USERS = {
    "test-device-123": {"prompts_used": 0, "plan": "free"}
}

@app.post("/api/v1/tasks/execute")
async def execute_task(
    request: TaskRequest,
    device_id: Optional[str] = Header(None)
):
    """Execute a task using YOUR API keys"""
    
    # For testing, allow anonymous with device ID
    if not device_id:
        device_id = "test-device-123"
    
    # Check usage limits
    user = MOCK_USERS.get(device_id, {"prompts_used": 0, "plan": "free"})
    
    if user["plan"] == "free" and user["prompts_used"] >= 5:
        raise HTTPException(
            status_code=429,
            detail="Free prompts exhausted. Create account: nexus --signup"
        )
    
    # Get YOUR API keys from environment (never exposed to user)
    gemini_key = os.getenv("NEXUS_PRIMARY_KEYS", "").split(",")[0]
    grok_key = os.getenv("NEXUS_SECONDARY_KEYS", "").split(",")[0]
    
    if not gemini_key or not grok_key:
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: API keys not set"
        )
    
    # TODO: Actually call AI models here
    # For now, mock response
    result = f"✓ Task executed: {request.task}\n\n(This is a mock response. Connect real AI models to see actual results.)"
    
    # Update usage
    user["prompts_used"] += 1
    MOCK_USERS[device_id] = user
    
    return TaskResponse(
        success=True,
        result=result,
        prompts_remaining=5 - user["prompts_used"]
    )

@app.get("/api/v1/health")
async def health():
    """Health check"""
    return {"status": "ok", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

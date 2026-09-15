import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
from agent import TaskAgent

load_dotenv()

app = FastAPI(title="Module 7 - Anthropic Tool-Using Agent", version="1.0.0")

agent = TaskAgent(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6"),
)

class AgentRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "Module 7 Anthropic Agent API is running"}

@app.get("/tools")
def list_tools():
    return {"tools": ["get_task", "list_tasks", "calculate"]}

@app.post("/agent/run")
async def run_agent(request: AgentRequest):
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY is not configured in .env")
    try:
        return await agent.run(request.prompt)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

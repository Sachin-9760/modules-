import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel

from providers.openai_provider import OpenAIProvider
from providers.claude_provider import ClaudeProvider
from providers.ollama_provider import OllamaProvider
from services.ai_service import AIService

load_dotenv()

app = FastAPI(title="Module 6 Provider-Agnostic AI API", version="1.0.0")


class AIRequest(BaseModel):
    provider: str
    prompt: str


def get_provider(name: str):
    name = name.lower()

    if name == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-5-mini")
        if not api_key:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")
        return OpenAIProvider(api_key, model)

    if name == "claude":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")
        if not api_key:
            raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY is not configured")
        return ClaudeProvider(api_key, model)

    if name == "ollama":
        model = os.getenv("OLLAMA_MODEL", "llama3.2")
        return OllamaProvider(model)

    raise HTTPException(
        status_code=400,
        detail="Unsupported provider. Use openai, claude, or ollama."
    )


@app.get("/")
def home():
    return {"message": "Module 6 AI Provider API is running"}


@app.get("/providers")
def providers():
    return {
        "providers": ["openai", "claude", "ollama"],
        "usage": "POST /ai/generate"
    }


@app.post("/ai/generate")
async def generate(request: AIRequest):
    provider = get_provider(request.provider)
    service = AIService(provider, request.provider)

    try:
        return await service.generate(request.prompt)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

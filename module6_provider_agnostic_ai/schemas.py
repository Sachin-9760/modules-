from pydantic import BaseModel


class NormalizedAIResponse(BaseModel):
    provider: str
    model: str
    response: str
    latency_ms: float
    usage: dict | None = None

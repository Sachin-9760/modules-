import time
from providers.base import AIProvider


class AIService:
    def __init__(self, provider: AIProvider, provider_name: str):
        self.provider = provider
        self.provider_name = provider_name

    async def generate(self, prompt: str):
        start = time.perf_counter()

        result = await self.provider.generate(prompt)

        latency_ms = round((time.perf_counter() - start) * 1000, 2)

        return {
            "provider": self.provider_name,
            "model": result.get("model", "unknown"),
            "response": result["response"],
            "latency_ms": latency_ms,
            "usage": result.get("usage")
        }

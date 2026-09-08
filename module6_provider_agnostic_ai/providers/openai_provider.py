from openai import AsyncOpenAI
from .base import AIProvider


class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str):
        self.client = AsyncOpenAI(api_key=api_key, timeout=60.0, max_retries=2)
        self.model = model

    async def generate(self, prompt: str) -> dict:
        response = await self.client.responses.create(
            model=self.model,
            input=prompt
        )

        usage = None
        if getattr(response, "usage", None):
            usage = {
                "input_tokens": getattr(response.usage, "input_tokens", None),
                "output_tokens": getattr(response.usage, "output_tokens", None),
                "total_tokens": getattr(response.usage, "total_tokens", None)
            }

        return {
            "model": self.model,
            "response": response.output_text,
            "usage": usage
        }

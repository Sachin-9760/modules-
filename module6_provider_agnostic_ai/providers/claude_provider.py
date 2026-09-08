from anthropic import AsyncAnthropic
from .base import AIProvider


class ClaudeProvider(AIProvider):
    def __init__(self, api_key: str, model: str):
        self.client = AsyncAnthropic(api_key=api_key, timeout=60.0, max_retries=2)
        self.model = model

    async def generate(self, prompt: str) -> dict:
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        text = ""
        for block in response.content:
            if getattr(block, "type", None) == "text":
                text += block.text

        usage = None
        if getattr(response, "usage", None):
            usage = {
                "input_tokens": getattr(response.usage, "input_tokens", None),
                "output_tokens": getattr(response.usage, "output_tokens", None)
            }

        return {
            "model": self.model,
            "response": text,
            "usage": usage
        }

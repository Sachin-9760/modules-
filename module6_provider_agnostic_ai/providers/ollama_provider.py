import httpx
from .base import AIProvider


class OllamaProvider(AIProvider):
    def __init__(self, model: str):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    async def generate(self, prompt: str) -> dict:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            data = response.json()

        usage = {
            "input_tokens": data.get("prompt_eval_count"),
            "output_tokens": data.get("eval_count")
        }

        return {
            "model": self.model,
            "response": data.get("response", ""),
            "usage": usage
        }

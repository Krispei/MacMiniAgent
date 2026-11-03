from ollama import AsyncClient

class Model:
    def __init__(self, model_name: str):
        self.client = AsyncClient()
        self.model_name = model_name

    async def generate(self, messages: list[dict], think=False) -> str:
        response = await self.client.chat(
            model=self.model_name,
            messages=messages,
            think=think
        )
        return response.message.content or ""

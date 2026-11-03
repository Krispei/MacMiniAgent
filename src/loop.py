class Agent:
    def __init__(self, model):
        self.model=model
        self.messages=[]

    async def run(self, user_input: str) -> str:
        self.messages.append({
            "role": "user",
            "content": user_input
        })

        response = await self.model.generate(self.messages)

        self.messages.append({
            "role": "assistant",
            "content": response
        })

        return response
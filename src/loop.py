from memory.working import WorkingMemroy

class Agent:
    def __init__(self, model):
        self.model=model
        self.workingMemory = WorkingMemroy(10)

    async def run(self, user_input: str) -> str:
        self.workingMemory.add({
            "role": "user",
            "content": user_input
        })

        response = await self.model.generate(self.workingMemory.get())

        self.workingMemory.add({
            "role": "assistant",
            "content": response
        })

        return response
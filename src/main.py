from model import Model
from loop import Agent
import asyncio

MODEL = "qwen3.8:27b"

model = Model(MODEL)
agent = Agent(model=model, max_tool_limit=5)

async def main():
    while True:
        user_input = await asyncio.to_thread(input, "You: ")

        if user_input.lower() == "exit":
            break

        response = await agent.run(user_input=user_input)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    asyncio.run(main())
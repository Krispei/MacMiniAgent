from model import Model
from loop import Agent
from MCP.MCP_manager import MCPManager
from mcp import StdioServerParameters
import sys
import asyncio

MODEL = "qwen3.8:27b-mlx"

async def main():

    servers = create_servers()

    async with MCPManager(servers=servers) as mcp:

        model = Model(MODEL)
        agent = Agent(model=model, max_tool_limit=10, MCPManager=mcp)

        await agent.register_mcp_tools()

        while True:
            user_input = await asyncio.to_thread(input, "You: ")

            if user_input.lower() == "exit":
                break

            response = await agent.run(user_input=user_input)
            print(f"Assistant: {response}")

def create_servers():

    repo_path = "/Users/wonupark/Desktop/MacMiniAgent"
    
    servers = {
        "git": StdioServerParameters(
            command=sys.executable,
            args=[
                "-m",
                "mcp_server_git",
                "--repository",
                repo_path,
            ],
        ),
    }

    return servers

if __name__ == "__main__":
    asyncio.run(main())
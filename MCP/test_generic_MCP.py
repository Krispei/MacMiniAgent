from MCP.generic_MCP_client import MCPClient
import asyncio
import sys
from mcp import StdioServerParameters

async def t_tools():
    repo = "/Users/wonupark/Desktop/MacMiniAgent"

    git_config = StdioServerParameters(
        command=sys.executable,
        args=[
            "-m",
            "mcp_server_git",
            "--repository",
            repo,
        ],
    )

    async with MCPClient(git_config) as client:
        tools = await client.list_tools()
        print(tools)
        
if __name__ == "__main__":
    asyncio.run(t_tools())
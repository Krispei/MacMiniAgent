import asyncio
import sys
from pathlib import Path

from mcp import StdioServerParameters
from MCP.MCP_manager import MCPManager


async def main():
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

    async with MCPManager(servers) as manager:
        tools = await manager.list_tools()

        print("Available tools:")
        for tool in tools:
            print(tool["name"])

        result = await manager.call_tool(
            "git__git_status",
            {"repo_path": repo_path},
        )

        for block in result.content:
            if block.type == "text":
                print(block.text)


asyncio.run(main())

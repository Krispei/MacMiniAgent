import asyncio
from time import sleep
from mcp import Client, StdioServerParameters

class MCPClient:
    def __init__(self, server_params: StdioServerParameters):
        self.server_params = server_params
        self.client = Client(self.server_params)

    async def __aenter__(self):
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.__aexit__(exc_type, exc, tb)

    async def list_tools(self):
        result = await self.client.list_tools()
        return result.tools

    async def call_tool(self, name: str, arguments: dict):
        return await self.client.call_tool(
            name=name,
            arguments=arguments
        )
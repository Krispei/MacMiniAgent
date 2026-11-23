import inspect
import asyncio

class ToolRegistry:
    def __init__(self, mcp_manager=None):
        self.native_tools = {}
        self.mcp_manager = mcp_manager
        self.mcp_tool_names = set()
        self.mcp_schemas = []

    def register_native(self, func):
        """Registers native (non MCP) tools
        """
        if func.__name__ in self.native_tools:
            raise ValueError(f"Duplicate native tools: {func.__name__}")

        self.native_tools[func.__name__] = func

    def get_schema(self):
        return [*self.tools.values(), *self.mcp_schemas]

    async def register_mcp_tools(self):
        """ Registers MCP tools
        TODO: add duplicate checking / collision with native tools
        """

        if self.mcp_manager is None:
            return

        self.mcp_schemas = await self.mcp_manager.get_ollama_tools()
        self.mcp_tool_names = set([tool["function"]["name"] for tool in self.mcp_schemas])

    async def execute(self, name, arguments):
        if name in self.native_tools:
            func = self.native_tools[name]

            if inspect.iscoroutinefunction(func):
                return await func(**arguments)

            return await asyncio.to_thread(
                func, **arguments
            ) 

        if name in self.mcp_tool_names:
            return await self.mcp_manager.call_tool(
                name, arguments
            )

        raise ValueError(f"Unknown tool: {name}")
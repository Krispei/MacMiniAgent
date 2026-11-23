import inspect
import asyncio
from logger import logger

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

        logger.info("Registered native tool: %s", func.__name__)
        
        self.native_tools[func.__name__] = func

    def get_schema(self):
        return [*self.native_tools.values(), *self.mcp_schemas]

    async def register_mcp_tools(self):
        """ Registers MCP tools
        TODO: add duplicate checking / collision with native tools
        """

        if self.mcp_manager is None:
            return

        self.mcp_schemas = await self.mcp_manager.get_ollama_tools()

        mcp_tool_names = []

        for tool in self.mcp_schemas:
            mcp_tool_names.append(tool["function"]["name"])
            logger.info("Registered MCP tool: %s", tool["function"]["name"])
        
        self.mcp_tool_names = set(mcp_tool_names)

    async def execute(self, name, arguments):

        logger.info("Attempting to execute function: %s with arguments: %s", name, arguments)

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
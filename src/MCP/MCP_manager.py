from contextlib import AsyncExitStack

from MCP.generic_MCP_client import MCPClient

class MCPManager:
    def __init__(self, servers: dict):

        #maps servers to connection configs
        self.servers = servers

        #maps server. names to connected MCPClient objects
        self.clients = dict()

        #maps exposed tool names to the original (server, original name)
        self.tool_routes = {}

    async def __aenter__(self):
        self.exit_stack = AsyncExitStack()

        try:
            async with self.exit_stack:
                for server_name, params in self.servers.items():
                    client = await self.exit_stack.enter_async_context(MCPClient(params))

                    self.clients[server_name] = client

                self.exit_stack = self.exit_stack.pop_all()

        except BaseException:
            self.clients.clear()
            self.exit_stack = None
            raise

        return self

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if self.exit_stack is not None:
                return await self.exit_stack.__aexit__(
                    exc_type, exc, tb
                )
        finally:
            self.clients.clear()
            self.tool_routes.clear()
            self.exit_stack = None

    async def list_tools(self):
        """list_tools does two things: It calls list_tools to every available client 
        in the current session to rebuild self.tool_routes, and then it returns a list of tool names
        with the description and input schema.
        """
        self.tool_routes.clear()

        tools = []

        for server_name in self.clients.keys():

            server_tools = await self.clients[server_name].list_tools()

            for tool in server_tools:

                exposed_name = f"{server_name}__{tool.name}"

                # We already have one layer of protection here by using the server name attached with
                # the tool name, so this raises an error if thats not enough
                if exposed_name in self.tool_routes:
                    raise ValueError(f"Duplicate tool: {exposed_name}")

                self.tool_routes[exposed_name] = (server_name, tool.name)

                tools.append({
                    "name": exposed_name,
                    "description": tool.description,
                    "input_schema": tool.input_schema,
                })

        return tools

    async def call_tool(self, name: str, arguments: dict):
        """Routes the tool name to its origin MCP client and then calls the tool within that client"""
        
        if name not in self.tool_routes:
            raise ValueError(f"Unknown MCP tool: {name}")

        server_name, original_tool_name = self.tool_routes[name]

        return await self.clients[server_name].call_tool(original_tool_name, arguments)

    async def get_ollama_tools(self):
        """formats the MCP tools in a way ollama can understand"""
        
        mcp_tools = await self.list_tools()

        ollama_tools = []

        for tool in mcp_tools:
            ollama_tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"] or "",
                        "parameters": tool["input_schema"],
                    },
                }
            )

        return ollama_tools
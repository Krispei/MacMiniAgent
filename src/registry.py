from tools.calculator import calculate
import inspect

class ToolRegistry:
    def __init__(self):
        self.tools = {}

        self.register(calculate)

    def register(self, func):
        self.tools[func.__name__] = func

    def get_schema(self):
        return list(self.tools.values())

    async def execute(self, name, arguments):
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")

        func = self.tools[name]
        result = func(**arguments)

        if inspect.isawaitable(result):
            result = await result

        return result
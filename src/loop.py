from memory.working import WorkingMemroy
from memory.semantic import SemanticMemory
from registry import ToolRegistry
from tools.calculator import calculate
from tools.semantic_memory_tools import MemoryTools
from prompts import SYSTEM_PROMPT

class Agent:
    def __init__(self, model, max_tool_limit):
        self.model=model
        self.workingMemory = WorkingMemroy(max_messages=10)
        self.semanticMemory = SemanticMemory(db_path="src/memory/data/semantic.json")
        self.registry = ToolRegistry()

        #Registering tools
        self.registry.register(calculate)
        semantic_memory_tools = MemoryTools(SemanticMemory=self.semanticMemory)

        self.registry.register(func=semantic_memory_tools.save_memory)
        self.registry.register(func=semantic_memory_tools.remove_memory)
        self.registry.register(func=semantic_memory_tools.update_memory)
        self.registry.register(func=semantic_memory_tools.search_memory)

        self.max_tool_limit = max_tool_limit

    async def run(self, user_input: str) -> str:

        relevant_memories = self.semanticMemory.search(user_input, 2)

        formatted_memories = "\n".join(f" - {m["content"]}" for m in relevant_memories)

        if formatted_memories:
            print(f"LOG: memories:\n{formatted_memories}")

        sys = f"""
        {SYSTEM_PROMPT}
        """

        self.workingMemory.add({
            "role": "user",
            "content": user_input
        })

        for _ in range(self.max_tool_limit):

            conversation = [
                {"role": "system", "content": sys},
                *self.workingMemory.get()
            ]
            
            response = await self.model.generate(
                messages=conversation,
                tools=self.registry.get_schema()
            )

            self.workingMemory.add({
                "role": "assistant",
                "content": response.message.content
            })

            if not response.message.tool_calls:
                return response.message.content

            for tool_call in response.message.tool_calls:
                name = tool_call.function.name
                arguments = tool_call.function.arguments

                print(f"LOG: Executing: {name}({arguments})")

                try:
                    result = await self.registry.execute(
                        name=name,
                        arguments=arguments
                    )
                    print(result)
                except Exception as e:
                    result = f"Tool error: {e}"

                self.workingMemory.add({
                    "role": "tool",
                    "tool_name": name,
                    "content": str(result)
                })

        return "Tool iteration limit reached."

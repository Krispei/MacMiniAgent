from src.memory.working import WorkingMemroy
from src.memory.semantic import SemanticMemory
from src.registry import ToolRegistry
from src.tools.calculator import calculate
from src.tools.semantic_memory_tools import MemoryTools
from src.tools.filesystem_tools import FilesystemTools
from src.logger import logger
from src.prompts import SYSTEM_PROMPT
import json

class Agent:
    def __init__(self, model, max_tool_limit):
        self.model=model
        self.workingMemory = WorkingMemroy(max_messages=15)
        self.semanticMemory = SemanticMemory(db_path="src/memory/data/semantic.json")
        self.fileSystemTools = FilesystemTools(vault_path="/Users/wonupark/Desktop/vault")
        self.registry = ToolRegistry()

        #Registering tools
        self.registry.register(calculate)
        semantic_memory_tools = MemoryTools(SemanticMemory=self.semanticMemory)

        self.registry.register(func=semantic_memory_tools.save_memory)
        self.registry.register(func=semantic_memory_tools.remove_memory)
        self.registry.register(func=semantic_memory_tools.update_memory)
        self.registry.register(func=semantic_memory_tools.search_memory)

        self.registry.register(func=self.fileSystemTools.list_files)
        self.registry.register(func=self.fileSystemTools.read_file)


        logger.info("Tools registered")

        self.max_tool_limit = max_tool_limit

        logger.info(f"max_tool_limit = {max_tool_limit}")

    async def run(self, user_input: str) -> str:
        
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

            logger.info(f"Model Input: {conversation}")
            
            response = await self.model.generate(
                messages=conversation,
                tools=self.registry.get_schema(),
                think=True
            )

            self.log_response(response=response)
            
            self.workingMemory.add({
                "role": "assistant",
                "content": response.message.content
            })

            if not response.message.tool_calls:
                return response.message.content

            for tool_call in response.message.tool_calls:
                name = tool_call.function.name
                arguments = tool_call.function.arguments

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

    def log_response(self, response):

        ns = 10e9

        thinking_content = response.message.thinking.replace("\\n", "\n")
        output_content = response.message.content.replace("\\n", "\n")

        model = response.model

        load_duration_sec = response.load_duration / ns
        total_duration_sec = response.total_duration / ns

        num_input_tokens = response.prompt_eval_count
        input_duration_sec = response.prompt_eval_duration / ns

        input_tokens_per_sec = num_input_tokens/input_duration_sec


        num_output_tokens = response.eval_count
        output_duration_sec = response.eval_duration / ns

        output_tokens_per_sec = num_output_tokens/output_duration_sec


        logger.info("Thinking content:\n%s",
                thinking_content
        )

        logger.info("Output content:\n%s",
                output_content
        )
        
        logger.info("Model: %s",
                model
        )

        logger.info("Load duration: %.2f | Total duration %.2f",
                load_duration_sec,
                total_duration_sec,
        )       
                    
        logger.info("Num input tokens: %d | prefill (s) %.2fs | %.2f tok/sec",
                num_input_tokens,
                input_duration_sec,
                input_tokens_per_sec
        )

        logger.info("Num output tokens: %d | decode (s) %.2fs | %.2f tok/sec",
                num_output_tokens,
                output_duration_sec,
                output_tokens_per_sec
        )
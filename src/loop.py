from memory.working import WorkingMemroy
from memory.semantic import SemanticMemory

from registry import ToolRegistry

from tools.calculator import calculate
from tools.semantic_memory_tools import MemoryTools
from tools.filesystem_tools import FilesystemTools

from filesystem.filesystem import FileSystem


from logger import logger
from prompts import SYSTEM_PROMPT
import json

class Agent:
    def __init__(self, model, max_tool_limit, MCPManager):
        self.model=model
        self.workingMemory = WorkingMemroy(max_messages=50)
        self.semanticMemory = SemanticMemory(db_path="src/memory/data/semantic.json")
        self.FileSystem = FileSystem(vault_path="/Users/wonupark/Desktop/vault")
        self.registry = ToolRegistry(mcp_manager=MCPManager)

        #Registering tools
        semantic_memory_tools = MemoryTools(SemanticMemory=self.semanticMemory)
        filesystem_tools = FilesystemTools(self.FileSystem)

        self.registry.register_native(func=semantic_memory_tools.save_memory)
        self.registry.register_native(func=semantic_memory_tools.remove_memory)
        self.registry.register_native(func=semantic_memory_tools.update_memory)
        self.registry.register_native(func=semantic_memory_tools.search_memory)

        self.registry.register_native(func=filesystem_tools.list_files)
        self.registry.register_native(func=filesystem_tools.read_file)
        self.registry.register_native(func=filesystem_tools.create_file)
        self.registry.register_native(func=filesystem_tools.edit_file)
        
        self.max_tool_limit = max_tool_limit

    async def register_mcp_tools(self):
        await self.registry.register_mcp_tools()

    async def run(self, user_input: str) -> str:
        
        sys = SYSTEM_PROMPT

        logger.debug(sys)
        
        self.workingMemory.add({
            "role": "user",
            "content": user_input
        })

        for _ in range(self.max_tool_limit):
            
            conversation = [
                {"role": "system", "content": sys},
                *self.workingMemory.get()
            ]

            logger.info(self.workingMemory.get())

            response = await self.model.generate(
                messages=conversation,
                tools=self.registry.get_schema(),
                think=True
            )

            self.log_response(response=response)
            
            msg = {
                "role": "assistant",
                "content": response.message.content or ""
            }

            if response.message.thinking:
                msg["thinking"] = response.message.thinking
            
            if not response.message.tool_calls:
                self.workingMemory.add(msg)
                return response.message.content
            else:
                msg["tool_calls"] = [
                    {"function" : {"name": tc.function.name, "arguments": tc.function.arguments}} for tc in response.message.tool_calls
                ]

            self.workingMemory.add(msg)

            for tool_call in response.message.tool_calls:
                name = tool_call.function.name
                arguments = tool_call.function.arguments

                try:
                    result = await self.registry.execute(
                        name=name,
                        arguments=arguments
                    )
                except Exception as e:
                    result = f"Tool error: {e}"

                self.workingMemory.add({
                    "role": "tool",
                    "tool_name": name,
                    "content": str(result)
                })

        return "Tool iteration limit reached."

    def log_response(self, response):

        ns = 1e9

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
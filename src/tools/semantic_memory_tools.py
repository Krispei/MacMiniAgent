class MemoryTools:
    def __init__(self, SemanticMemory):
        self.SemanticMemory = SemanticMemory

    def save_memory(self, content: str) -> str:
        """
        Store new information in long-term semantic memory

        Use when the user explicitly or implicitly asks to remember something,
        or shares durable information useful in future conversations.

        Do not use to:
            - Store temporary conversation details
            - Modify an existing memory; use update_memory instead
            - Store duplicate information
            - Store information that has already been stored as a memory previously in the conversation

        Args:
            content: A self-contained factual statement to store.
        
        Returns:
            Identifier of the newly created memory (memory ID)
        """

        return self.SemanticMemory.save(content)

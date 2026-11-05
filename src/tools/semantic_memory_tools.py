class MemoryTools:
    def __init__(self, SemanticMemory):
        self.SemanticMemory = SemanticMemory

    def save_money(self, content: str) -> str:
        """ Tool calling docstring
        
        """

        self.SemanticMemory.save(content)

    def search_memory(self, query: str) -> list:
        """ Tool calling docstring
        
        """

        return self.SemanticMemory.seach(query)

    def delete_memory(self, memory_id: str) -> list:
        
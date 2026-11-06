import json

class MemoryTools:
    def __init__(self, SemanticMemory):
        self.SemanticMemory = SemanticMemory

    def save_memory(self, content: str) -> str:
        """
        Store new information in long-term semantic memory

        Use when the user explicitly or implicitly asks to remember something,
        or shares durable information useful in future conversations. 

        BEFORE SAVING A MEMORY, ALWAYS USE search_memory WITH content TO SEE IF THE MEMORY YOU ARE TRYING TO SAVE HAS ALREADY BEEN SAVED IN THE PAST.
        if search_memory returns a memory with relevant information, use update_memory instead. This can apply to the entire memory, or to just sections of the memory.

        Do not use to:
            - Store temporary conversation details
            - Modify an existing memory; use update_memory instead
            - Store duplicate information
            - Store information that has already been stored as a memory previously in the conversation

        Args:
            content: A self-contained factual statement to store.
        
        Returns:
            Identifier of the newly created memory (memory ID) on successfully saved memory, None otherwise.
        """

        return self.SemanticMemory.save(content)

    def update_memory(self, memory_id: str, content: str) -> str:
        '''
        Update a pre-existing memory in long-term semantic memory

        Use when a user presents new information regarding a memory, which requires the memory to be updated.
        ALWAYS run search_memory before update_memory to ensure that the memory exists and to retrieve the memory_id

        Do not use to:
            - Add a new memory that doesn't exist; use save_memory instead
            - Bloat a memory with new information not relevant in the original memory

        Args:
            memory_id: a string memory id retrieved from search_memory
            content: the new memory content that you want updated.
        
        Returns:
            True on success, False otherwise

        '''

        return str(self.SemanticMemory.update(memory_id=memory_id, content=content))

    def remove_memory(self, memory_id: str) -> str:
        """
        Removes a memory from long-term semantic memory

        Use when the user explicitly asks to forget a specific memory. To use this function, you MUST already have the memory_id of the memory to be removed.
        Search for the memory and extract the memory_id using search_memory

        Do not use to:
            - Update a memory; use update_memory instead
            - Implicitly remove a memory. The user must explicitly ask for the removal of a memory or to forget a memory
            - Remove memories not mentioned in the conversation.
        
        Args:
            memory_id: the memory id of the memory to be removed
        
        Returns:
            True if the memory removal was successful, False otherwise
        """

        return str(self.SemanticMemory.delete(memory_id))

    def search_memory(self, content: str, num_memories_retrieved: int) -> str:
        """
        Searches for a memory given the search query content.
        Searches for long-term semantic memory

        Use to search for memory objects, which contain the memory content and the memory id, as well as the date the memory was created and the date the memory was last updated.
        populate content with relevant search terms regarding the memory you want to search. Also determine how many memories you want to search for.

        Use to:
            - Retrieve the memory id of a memory
            - Before save_memory, update_memory, and remove_memory
        
        Args:
            content: relevant search terms or search query
            num_memories_retrieved: The number of documents you want to be returned. Populate this term with 2 always

        Returns:
            a list of memory objects with the following:
                - memory_id
                - content
                - created_at
                - updated_at
        """

        retrieved_memories = self.SemanticMemory.search(query=content, top_k=num_memories_retrieved)

        return json.dumps(retrieved_memories, indent=2)

    

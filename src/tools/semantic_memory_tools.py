import json
from memory.semantic import MemoryNotFoundError
from retrieval.embed import EmbeddingError
from tools.tool_reporter import create_report

class MemoryTools:
    def __init__(self, SemanticMemory):
        self.SemanticMemory = SemanticMemory

    def save_memory(self, content: str) -> str:
        """
        Store new information in long-term semantic memory

        Use to store DURABLE, LONG-TERM memory. Use for facts that are not likely to change (persistent), for information about the user, etc.

        BEFORE SAVING A MEMORY, ALWAYS USE search_memory WITH content TO SEE IF THE MEMORY YOU ARE TRYING TO SAVE HAS ALREADY BEEN SAVED IN THE PAST.
        if search_memory returns a memory with relevant information, use update_memory instead. 
        
        memories should be broken down to their most individual parts. For example, If the user describes two things ("I like waffles and pancakes"), 
        this tool should be called twice, once for waffles and another for pancakes.

        Args:
            content (str): A self-contained factual statement to store.
        
        Returns:
            dict: A dictionary containing:
                - tool_call (str): the name of the tool called.
                - success (bool): True for successful tool call, False for unsuccessful tool call.
                - error (str | None): Error message if the tool call fails, otherwise None on successfull tool call
                - output (dict): Memory object that has been created, with the following keys:
                    - id (str): unique memory id.
                    - content (str): content of the memory that was saved
                    - created_at (str): date of creation
                    - updated_at (str): date of last update.

        Restrictions:
            - Do not use to store temporary conversation details or non-durable information (such as: "today is friday", "Tomorrow I will go to the park", etc)
            - This tool should not be used to modify an existing memory; use update_memory instead.
            - Do not store duplicate information, nor rewordings or paraphrases of existing memories
            - Do not store information that has already been stored as a memory previously in the conversation.
        """

        try:
            memory = self.SemanticMemory.save(content)
            return create_report(
                tool_call="save_memory",
                success=True,
                error=None,
                output=memory
            )
        except EmbeddingError as e:
            return create_report(
                tool_call="save_memory",
                success=False,
                error=str(e),
                output=None
            )


    def update_memory(self, memory_id: str, content: str) -> str:
        '''
        Update a pre-existing memory in long-term semantic memory

        Use when a user presents new information regarding a memory that has already been saved, which requires the memory to be updated.
        ALWAYS run search_memory before update_memory to ensure that the memory exists and to retrieve the memory_id

        Do not use to:
            - Add a new memory that doesn't exist; use save_memory instead
            - Bloat a memory with new information not relevant in the original memory

        Args:
            memory_id: a string memory id retrieved from search_memory
            content: the new memory content that you want updated.
        
        Returns:
            "status", "report", and the updated memory object, describing whether the memory was successfully updated or not.
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
            "status" and "report" indicating whether the removal was successful 
        """

        return str(self.SemanticMemory.delete(memory_id))

    def search_memory(self, content: str, num_memories_retrieved: int) -> str:
        """
        Searches for a memory given the search query content.
        Searches for long-term semantic memory. 
        Search uses BM25 Keyword search and Vector search, so populate content with both keywords and semantic meaning if applicable.


        Use to search for memory objects, which contain the memory content and the memory id, as well as the date the memory was created and the date the memory was last updated.
        populate content with relevant search terms regarding the memory you want to search. Also determine how many memories you want to search for.

        Use to:
            - Retrieve the memory id of a memory
            - Before save_memory, update_memory, and remove_memory
        
        Args:
            content: relevant search terms or search query
            num_memories_retrieved: The number of documents you want to be returned. Populate this term with anywhere from 1-3

        Returns:
            memory objects with the following:
                - memory_id
                - content
                - created_at
                - updated_at
            The dict will also describe whether the content came from BM25 or from vector search.
        """

        retrieved_memories = self.SemanticMemory.search(query=content, top_k=num_memories_retrieved)

        return json.dumps(retrieved_memories, indent=2)

    

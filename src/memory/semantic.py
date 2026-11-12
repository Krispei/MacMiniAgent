import json
import uuid
import numpy as np
from datetime import datetime, timezone
from retrieval.BM25 import BM25Search
from retrieval.embed import embed_document
from retrieval.embed import embed_query
from retrieval.KNN import KNN
from pathlib import Path

class MemoryNotFoundError(LookupError):
    pass

class SemanticMemory:
    def __init__(self, db_path):
        self.db_path = db_path 
        self.BM25index = BM25Search()
        self.ids = self._get_ids()

        memories = self._load_memories()
        self.BM25index.build(memories)

    def save(self, content: str):
        '''saves a memory into the semantic memory database + creates embedding
        
        memories are dicts with the following keys:
            - id: memory id
            - content: text memory content
            - created_at: date created
            - updated_at: date last updated

        Args:
            content: String text of memory content

        Returns:
            memory : dict
        '''

        embedding = embed_document(content=content)[0].tolist()

        memory = {
            "id": str(uuid.uuid4()),
            "content": content,
            "embedding": embedding,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        memories = self._load_memories()
        memories.append(memory)

        self.ids.add(memory["id"])
        self._persist_memories(memories=memories)

        return self._strip_embedding_for_return(memories=[memory])

    def search(self, query: str, top_k=3) -> dict:
        '''Uses BM25 + embedding search to retrieve top_k relevant documents
        
        Args:
            query: text query to search for
            top_k: k number of documents requested. DEFAULT 3

        Returns:
            dict(List[]) containing keys:
                "BM25" : list of memory objects retrieved from BM25 search
                "Vector seach" : list of memory objects retrieved from vector search
        '''

        memories = self._load_memories()

        retrieved = {
            "BM25" : None,
            "Vector search": None
        }

        if not memories:
            retrieved

        self.BM25index.build(memories)

        memories_BM25 = self.BM25index.search(query=query, top_k=top_k)
        memories_vector = self._vector_search(query=query, top_k=top_k)

        formatted_BM25_memories = self._strip_embedding_for_return(memories=memories_BM25)
        formatted_vector_memories = self._strip_embedding_for_return(memories=memories_vector)

        retrieved["BM25"] = formatted_BM25_memories
        retrieved["Vector search"] = formatted_vector_memories

        return retrieved


    def update(self, memory_id: str, content: str) -> bool:
        '''updates a memory's content given a memory id
        
        Args:
            memory_id : string memory id
            content : updated memory content
        
        Returns:
            the updated formatted memory object on success
        '''

        if memory_id not in self.ids:
            raise MemoryNotFoundError(f"Memory id not found: {memory_id}")
        
        memories = self._load_memories()
        updated_memory_embedding = embed_document(content=content)[0].tolist()

        updated_formatted_memory = None

        for memory in memories:
            if memory['id'] == memory_id:
                memory['content'] = content
                memory['embedding'] = updated_memory_embedding,
                memory['updated_at'] = datetime.now(timezone.utc).isoformat()
                updated_formatted_memory = self._strip_embedding_for_return(memories=[memory])
                break

        self._persist_memories(memories=memories)

        return updated_formatted_memory


    def delete(self, memory_id: str) -> bool:
        '''deletes a memory given a memory id
        
        Args:
            memory_id : string memory id
        
        Returns:
            True on success
        '''

        if memory_id not in self.ids:
            raise MemoryNotFoundError(f"Memory id not found: {memory_id}")

        memories = self._load_memories()

        new_memories = [m for m in memories if m['id'] != memory_id]

        self.ids.remove(memory_id)
        self._persist_memories(memories=new_memories) 

        return True

    def _get_ids_and_embeddings(self):
        '''Helper function to get the id and corresponding embedding of every memory
        '''

        memories = self._load_memories()

        ids, embeddings = [], []
        
        for i in range(len(memories)):
            ids.append(memories[i]["id"])
            embeddings.append(memories[i]["embedding"])

        return ids, embeddings

    def _vector_search(self, query: str, top_k: int) -> list[dict]:
        ''' Performs vector search on the semantic memory db

        Args:
            query: string query
            top_k: number of items to retrieve

        Returns:
            List[dict] list of UNFORMATTED memory objects
        '''

        ids, embeddings = self._get_ids_and_embeddings()

        #Handles Empty memory:
        if len(embeddings) == 0:
            return []

        ids = np.array(ids)
        embeddings = np.array(embeddings)

        query_embedding = embed_query(query=query)
        k_documents_idx = KNN(document_embeddings=embeddings, query_embedding=query_embedding, top_k=top_k)

        k_ids = ids[k_documents_idx]

        k_ids = k_ids.tolist()

        memories = self._load_memories()

        out = []

        for memory in memories:
            if memory['id'] in k_ids:
                out.append(memory)

        return out


    def _load_memories(self):
        '''Private helper function: loads memories (handles initially empty memory files)
        
        Args:
            None
        
        Returns:
            list[Dict]
        '''

        path = Path(self.db_path)
    
        if not path.exists() or path.stat().st_size == 0:
            return []
    
        with open(path, "r") as f:
            return json.load(f)
    
    def _persist_memories(self, memories) -> None:
        """Writes memories into semantic memory db

        Args:
            memories: list[dict] containing unformatted memory objects
        
        returns:
            None
        """

        path = Path(self.db_path)
    
        with open(path, "w", encoding="utf-8") as f:
            json.dump(memories, f, indent=4)
    
        self.BM25index.build(memories)

    def _strip_embedding_for_return(self, memories: list[dict]) -> list[dict]:
        """Strips the embedding from the memory object. Used before sending the memory object to the LLM to prevent context bloat

        Args:
            memories: list[dict], list of unformatted memory objects

        Returns:
            list[dict], list of FORMATTED memory objects with embedding removed.
        """

        stripped = []

        for memory in memories:
            stripped.append({key: memory[key] for key in memory if key != "embedding"})
        
        return stripped

    def _get_ids(self) -> set:
        """Helper function to get all ids for easy id lookup"""

        ids = set()
        for memory in self._load_memories():
            ids.add(memory["id"])

        return ids
    

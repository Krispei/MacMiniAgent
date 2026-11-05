import json
import uuid
from datetime import datetime, timezone
from retrieval.BM25 import BM25Search
from pathlib import Path

class SemanticMemory:
    def __init__(self, db_path):
        self.db_path = db_path 
        self.BM25index = BM25Search()

        memories = self._load_memories()
        self.BM25index.build(memories)

    def save(self, content):
        '''saves a memory into the semantic memory database
        
        memories are dicts with the following keys:
            - id: memory id
            - content: text memory content
            - created_at: date created
            - updated_at: date last updated

        Args:
            content: String text of memory content

        Returns:
            newly created memory ID
        '''

        memory = {
            "id": str(uuid.uuid4()),
            "content": content,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        memories = self._load_memories()
        memories.append(memory)

        self._persist_memories(memories=memories)

        return memory["id"]

    def search(self, query, top_k=5) -> list[dict]:
        '''Uses BM25 search to retrieve top_k relevant documents
        
        Args:
            query: text query to search for
            top_k: k number of documents requested. 

        Returns:
            list of memory dicts (see: self.save)
        '''

        return self.BM25index.search(query=query, top_k=top_k)

    def update(self, memory_id: str, content: str) -> bool:
        '''updates a memory's content given a memory id
        
        Args:
            memory_id : string memory id
            content : updated memory content
        
        Returns:
            True on Success, False on Failure 
        '''
        
        memories = self._load_memories()

        updated = False

        for memory in memories:
            if memory['id'] == memory_id:
                memory['content'] = content
                memory['updated_at'] = datetime.now(timezone.utc).isoformat()
                updated = True

        if updated:
            self._persist_memories(memories=memories)
            return True
        else:
            return False


    def delete(self, memory_id: str) -> bool:
        '''deletes a memory given a memory id
        
        Args:
            memory_id : string memory id
        
        Returns:
            True on success, False on Failure
        '''

        memories = self._load_memories()

        memories = [m for m in memories if m['id'] != memory_id]

        self._persist_memories(memories=memories)  


    def _load_memories(self):
        '''Private helper function: loads memories (handles initially empty memory files)
        
        '''
        path = Path(self.db_path)
    
        if not path.exists() or path.stat().st_size == 0:
            return []
    
        with open(path, "r") as f:
            return json.load(f)
    
    def _persist_memories(self, memories):
        path = Path(self.db_path)
    
        with open(path, "w", encoding="utf-8") as f:
            json.dump(memories, f, indent=4)
    
        self.BM25index.build(memories)


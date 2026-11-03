import json
import uuid
from datetime import datetime, timezone
from retrieval.BM25 import BM25Search

class SemanticMemory:
    def __init__(self, db_path):
        self.db_path = db_path 
        self.BM25index = BM25Search()

        with open(self.db_path, "r", encoding="utf-8") as f:
            memories = json.load(f)

        self.BM25index.build(memories)


    def save(self, content):

        memory = {
            "id": str(uuid.uuid4()),
            "content": content,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        with open(self.db_path, "r", encoding="utf-8") as f:
            memories = json.load(f)

        memories.append(memory)

        self.BM25index.build(memories)

        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(memories, f, indent=4)

    def search(self, query, top_k=5) -> list[dict]:
        '''Uses BM25 search to retrieve top_k relevant documents
        
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
        
        with open(self.db_path, "r", encoding="utf-8") as f:
            memories = json.load(f)

        updated = False

        for memory in memories:
            if memory['id'] == memory_id:
                memory['content'] = content
                memory['updated_at'] = datetime.now(timezone.utc).isoformat()
                updated = False

        if updated:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(memories, f, indent=4)
            self.BM25index.build(memories)
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

        with open(self.db_path, "r", encoding="utf-8") as f:
            memories = json.load(f)

        memories = [m for m in memories if m['id'] != memory_id]

        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(memories, f, indent=4)

        self.BM25index.build(memories)        

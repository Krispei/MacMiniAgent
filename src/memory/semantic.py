import json
import uuid
from datetime import datetime, timezone
from retrieval.BM25 import BM25Search
from retrieval.embed import embed_document
from retrieval.embed import embed_query
from pathlib import Path

class SemanticMemory:
    def __init__(self, db_path):
        self.db_path = db_path 
        self.BM25index = BM25Search()

        memories = self._load_memories()
        self.BM25index.build(memories)

    def save(self, content):
        '''saves a memory into the semantic memory database + creates embedding
        
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

        embedding = list(embed_document(content=content))

        memory = {
            "id": str(uuid.uuid4()),
            "content": content,
            "embedding": embedding,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        memories = self._load_memories()
        memories.append(memory)
        self._persist_memories(memories=memories)

        formatted_memory = self._strip_embedding_for_return(memory=memory)
        
        return {
            "result": "success",
            "report": "Memory successfully created",
            "memory": formatted_memory
        }

    def search(self, query, top_k=5) -> list[dict]:
        '''Uses BM25 + embedding search to retrieve top_k relevant documents
        
        Args:
            query: text query to search for
            top_k: k number of documents requested. 

        Returns:
            list of memory dicts (see: self.save)
        '''

        memories = self.BM25index.search(query=query, top_k=top_k)

        formatted_memories = [self._strip_embedding_for_return(memory=memory) for memory in memories]

        ret = {
            "status": None,
            "report": None,
            "memories": formatted_memories
        }

        if memories:
            ret['status'] = "success"
            ret['report'] = f"{len(memories)} memories found"
        else:
            ret['status'] = "failed",
            ret['report'] = "No memories found"

        return ret


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
        updated_formatted_memory = None

        for memory in memories:
            if memory['id'] == memory_id:
                memory['content'] = content
                memory['updated_at'] = datetime.now(timezone.utc).isoformat()
                updated = True
                updated_formatted_memory = self._strip_embedding_for_return(memory=memory)
                break

        ret = {
            "status": None,
            "report": None,
            "memory": updated_formatted_memory
        }

        if updated:
            self._persist_memories(memories=memories)
            ret["status"] = "success"
            ret["report"] = "Memory updated"
        else:
            ret["status"] = "failed"
            ret["report"] = "Memory not found, no memory updated"

        return ret


    def delete(self, memory_id: str) -> bool:
        '''deletes a memory given a memory id
        
        Args:
            memory_id : string memory id
        
        Returns:
            True on success, False on Failure
        '''

        memories = self._load_memories()

        new_memories = [m for m in memories if m['id'] != memory_id]

        self._persist_memories(memories=new_memories) 

        deleted = len(new_memories) == len(memories) - 1

        ret = {
            "status": None,
            "report": None,
        }

        if deleted:
            ret["status"] = "success"
            ret["report"] = "Memory successfully deleted."
        else:
            ret["status"] = "failed"
            ret["report"] = "Memory not found."

        return ret


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

    def _strip_embedding_for_return(self, memory: dict) -> dict:

        return {
            "id": memory['id'],
            "content": memory['content'],
            "created_at": memory["created_at"],
            "updated_at": memory["updated_at"],
        }
    

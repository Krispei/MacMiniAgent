import json
import uuid
import numpy as np
from datetime import datetime, timezone
from retrieval.BM25 import BM25Search
from retrieval.embed import embed_document
from retrieval.embed import embed_query
from retrieval.KNN import KNN
from pathlib import Path

class SemanticMemory:
    def __init__(self, db_path):
        self.db_path = db_path 
        self.BM25index = BM25Search()

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
            newly created memory ID
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
        self._persist_memories(memories=memories)

        formatted_memory = self._strip_embedding_for_return(memories=[memory])
        
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

        memories = self._load_memories()

        if not memories:
            return {
                "status": "failed",
                "report": "No memories currently exist",
                "memories": []
            }

        self.BM25index.build(memories)

        memories_BM25 = self.BM25index.search(query=query, top_k=top_k)
        memories_vector = self._vector_search(query=query, top_k=top_k)

        print("LOG: Memories found")

        formatted_BM25_memories = self._strip_embedding_for_return(memories=memories_BM25)
        formatted_vector_memories = self._strip_embedding_for_return(memories=memories_vector)

        retrieved = {   
            "BM25" : formatted_BM25_memories,
            "Vector search": formatted_vector_memories
        }

        ret = {
            "status": "success",
            "report": "Memories retrieved",
            "memories": retrieved
        }

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
                memory['embedding'] = list(embed_document(content=content))
                memory['updated_at'] = datetime.now(timezone.utc).isoformat()
                updated = True
                updated_formatted_memory = self._strip_embedding_for_return(memories=[memory])
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

    def _get_ids_and_embeddings(self):
        '''Helper function to get the id and corresponding embedding of every memory
        '''
        print(f"LOG: Function _get_ids_and_embeddings() called")

        memories = self._load_memories()

        ids, embeddings = [], []

        print(f"LOG: length of memories: {len(memories)}")
        
        for i in range(len(memories)):
            ids.append(memories[i]["id"])
            embeddings.append(memories[i]["embedding"])

        return ids, embeddings

    def _vector_search(self, query, top_k):
        '''
        quick note: returns memories
        '''
        print(f"LOG: Function _vector_search(query = {query}, top_k = {top_k}) called")

        ids, embeddings = self._get_ids_and_embeddings()

        #Handles Empty memory:
        if len(embeddings) == 0:
            return []

        print(f"LOG: ids: {ids}")

        ids = np.array(ids)
        embeddings = np.array(embeddings)

        print(f"LOG: embeddings shape: {embeddings.shape}")

        query_embedding = embed_query(query=query)

        k_documents_idx = KNN(vecs=embeddings, query_embedding=query_embedding, k=top_k)
        print(f"LOG: k_ids = {k_documents_idx}")

        k_ids = ids[k_documents_idx]

        
        k_ids = k_ids.tolist()

        memories = self._load_memories()

        out = []

        print(memories)

        for memory in memories:
            if memory['id'] in k_ids:
                out.append(memory)

        return out


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

    def _strip_embedding_for_return(self, memories: list[dict]) -> list[dict]:

        stripped = []

        for memory in memories:
            stripped.append({
                "id": memory['id'],
                "content": memory['content'],
                "created_at": memory["created_at"],
                "updated_at": memory["updated_at"],
            })
        
        return stripped
    

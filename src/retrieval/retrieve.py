from retrieval.embed import embed_query, embed_documents, get_document_embeddings
from retrieval.KNN import KNN

def retrieve(query: str, k: int) -> list[str]:
    """retrieves k chunks that should be the response to the query

    Args:
        query : LLM user query
        k : Number of chunks to retrieve

    Returns:
        k_paths : k pathnames corresponding to the k most relevant chunks (pathnames could be repeated, and is not returned in any particular order)
        k_chunks : k most relevant chunks (not returned in any particular order)
    """

    query_embedding = embed_query(query=query)

    sources, chunks, embeddings = get_document_embeddings()
    
    k_documents_idx = KNN(vecs=embeddings, query_embedding=query_embedding, k=k)

    k_paths = sources[k_documents_idx]
    k_chunks = chunks[k_documents_idx]

    k_chunks = k_chunks.tolist()
    k_paths = k_paths.tolist()

    return k_paths, k_chunks

def main():
    
    print(retrieve("What did I do on October 27th?", 3))

if __name__ == "__main__":
    main()
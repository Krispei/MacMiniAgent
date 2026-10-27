from embed import embed_query, embed_documents, get_document_embeddings
from KNN import KNN

def retrieve(query: str, k: int) -> list[str]:
    """
        Goal: query in, k most relevant document paths out.
    """

    query_embedding = embed_query(query=query)

    sources, embeddings = get_document_embeddings()
    
    k_documents_idx = KNN(vecs=embeddings, query_embedding=query_embedding, k=k)

    k_paths = sources[k_documents_idx]

    k_paths = k_paths.tolist()

    return k_paths

def main():
    
    print(retrieve("Hello", 4))

if __name__ == "__main__":
    main()
import numpy as np

def KNN(document_embeddings, query_embedding, top_k: int):
    """Performs K-Nearest neighbors with document vectors, query embedding, and top_k
    
    Args:
        document_embeddings: [N, D] embedding matrix containing N documents with embedding size D
        query_embedding: [D] embedding of query
        top_k : number of nearest neighbors desired for retrieval

    Returns:
        indicies of largest neighbors [k]
    """

    cos_sim = cosine_similarity(a=document_embeddings, b=query_embedding)

    N = document_embeddings.shape[0]

    k_nn = np.argpartition(cos_sim, max(-top_k, -1*N))[max(-top_k, -1*N):]
    
    return k_nn


def cosine_similarity(a, b):
    """Calculates cosine similarity

    Args:
        a: [N,D] numpy matrix containing N documents of hidden size D
        b: [D] vector 
    
    Returns:
        [N] vector containing the cosine similarity scores for each document versus b
    """


    dot_prod = a @ b.T #shape [N, 1]

    dot_prod = dot_prod.flatten()

    norm_a = np.linalg.norm(a, axis=1) # [N, 1]
    norm_b = np.linalg.norm(b)

    denom = norm_a * norm_b

    cos_sim = dot_prod / denom

    return cos_sim


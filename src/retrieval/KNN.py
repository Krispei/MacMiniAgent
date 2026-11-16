import numpy as np
from numpy.typing import ArrayLike

def KNN(document_embeddings, query_embedding, top_k: int):
    """Performs K-Nearest neighbors with document vectors, query embedding, and top_k
    
    Args:
        document_embeddings: [N, D] embedding matrix containing N documents with embedding size D
        query_embedding: [D] embedding of query
        top_k : number of nearest neighbors desired for retrieval

    Returns:
        indicies of largest neighbors [k]
    """

    if top_k == 0:
        return np.array([])

    if top_k < 0:
        raise ValueError

    cos_sim = cosine_similarity(a=document_embeddings, b=query_embedding)

    cos_sim = np.atleast_1d(cos_sim)

    N = document_embeddings.shape[0]
    print(cos_sim)
    k_nn = np.argpartition(cos_sim, max(-1*top_k, -1*N))[max(-1*top_k, -1*N):]
    
    return k_nn


def cosine_similarity(a: ArrayLike, b: ArrayLike):
    """Calculates cosine similarity

    Args:
        a: [N,D] or [D] numpy matrix containing N documents of hidden size D
        b: [D] vector 
    
    Returns:
        [N] vector containing the cosine similarity scores for each document versus b
    """

    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    eps = 1e-12
    dot_prod = a @ b.T

    dot_prod = dot_prod.flatten()

    norm_a = np.linalg.norm(a, axis=-1) 
    norm_b = np.linalg.norm(b)

    denom = norm_a * norm_b

    cos_sim = dot_prod / (denom + eps)

    return cos_sim


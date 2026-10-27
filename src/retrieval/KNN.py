import numpy as np

def KNN(vecs, query_embedding, k):
    '''
        args:

        vecs: [N, D] embedding matrix containing N chunks with embedding size D
        query_embedding: embedding of query
        k : number of nearest neighbors desired for retrieval

        returns:

        indicies of largest neighbors [k]
    '''

    cos_sim = cosine_similarity(vecs=vecs, query_embedding=query_embedding)

    k_nn = np.argpartition(cos_sim, -k)[-k:]

    return k_nn


def cosine_similarity(vecs, query_embedding):

    dot_prod = vecs @ query_embedding #shape [N, 1]

    norm_vecs = np.linalg.norm(vecs, axis=1) # [N, 1]
    norm_query = np.linalg.norm(query_embedding)

    denom = norm_vecs * norm_query

    cos_sim = dot_prod / denom

    return cos_sim


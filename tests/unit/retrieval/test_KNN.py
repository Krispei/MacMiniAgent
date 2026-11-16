from retrieval.KNN import KNN
import pytest
import numpy as np

def test_malformed_input():
    vector = np.array([1, 0, 2])

    matrix = np.array([[1, 0],
                       [3, 1],
                       [1, "2"],
                       [1, "a"],
                       [0, "string"],
                       [-1, 0],])

    with pytest.raises(ValueError):
        out = KNN(matrix,vector, 3)

def test_k_equals_0():
    vector = np.array([1, 0])

    matrix = np.array([[1, 0],
                       [3, 1],
                       [1, 1],
                       [1, 3],
                       [0, 1],
                       [-1, 0],])

    assert len(KNN(document_embeddings=matrix, query_embedding=vector, top_k=0)) == 0

def test_returns_k_indicies():
    vector = np.array([1, 0])

    matrix = np.array([[1, 0],
                       [3, 1],
                       [1, 1],
                       [1, 3],
                       [0, 1],
                       [-1, 0],])

    assert len(KNN(document_embeddings=matrix, query_embedding=vector, top_k=3)) == 3

def test_correct_indicies():
    vector = np.array([1, 0])

    matrix = np.array([[1, 0],
                       [-1, 0],
                       [3, 1],
                       [1, 1],
                       [1, 3],
                       [0, 1]])

    expected = np.array([1.0, -1.0, 0.948683, 0.707107, 0.316228, 0.0])

    ans = [np.array([0,2]), np.array([2,0])]

    assert any(np.allclose(KNN(matrix, vector, 2), a) for a in ans)

def test_largeK():
    vector = np.array([1, 0])

    matrix = np.array([[1, 0]])

    assert KNN(matrix,vector, 2) == np.array([0])
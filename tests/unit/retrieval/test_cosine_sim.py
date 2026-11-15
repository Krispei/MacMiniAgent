from retrieval.KNN import cosine_similarity
import numpy as np
import pytest

def test_identical_vectors():
    vec = np.array([5.0, 6.0, 7.0])

    assert cosine_similarity(vec, vec) == pytest.approx(1.0)

def test_zero_vector():
    vec1 = np.array([1.0, 2.0, 3.0])
    vec2 = np.array([0.0, 0.0, 0.0])

    assert cosine_similarity(vec1, vec2) == pytest.approx(0.0)

def test_two_zero_vectors():
    vec1 = np.array([0.0,0.0])
    vec2 = np.array([0.0,0.0])

    assert cosine_similarity(vec1, vec2) == pytest.approx(0.0)

def test_scaled_vectors():
    vec1 = np.array([5.0, 6.0, 7.0])
    vec2 = np.array([10.0, 12.0, 14.0])

    assert cosine_similarity(vec1, vec2) == pytest.approx(1.0)

def test_one_list_input():
    vec1 = np.array([1.0, 2.0, 3.0])
    vec2 = [1.0, 2.0, 3.0]

    assert cosine_similarity(vec1, vec2) == pytest.approx(1.0)

def test_two_list_input():
    vec1 = [1.0, 2.0, 3.0]
    vec2 = [1.0, 2.0, 3.0]

    assert cosine_similarity(vec1, vec2) == pytest.approx(1.0)

def test_invalid_input_int():
    vec1 = np.array([1.0, 2.0, 3.0])
    vec2 = 3

    with pytest.raises(ValueError):
        sim = cosine_similarity(vec1, vec2)

def test_invalid_input_str():
    vec1 = np.array([1.0, 2.0, 3.0])
    vec2 = "Hel"

    with pytest.raises(ValueError):
        sim = cosine_similarity(vec1, vec2)

def test_incorrect_dim_2vecs():
    vec1 = np.array([1.0, 2.0, 3.0])
    vec2 = np.array([1.0, 2.0])

    with pytest.raises(ValueError):
        sim = cosine_similarity(vec1, vec2)

def test_matrix_vec():
    matrix = np.array([[1.0,2.0,3.0],
                      [1.0,2.0,3.0],
                      [1.0,2.0,3.0]])
    vector = np.array([1.0, 2.0, 3.0])

    assert cosine_similarity(matrix, vector) == pytest.approx(np.array([1.0, 1.0, 1.0]))

def test_zero_matrix_vec():
    matrix = np.array([[0.0,0.0,0.0],
                       [1.0,2.0,3.0],
                       [0.0,0.0,0.0]])
    vector = np.array([1.0,2.0,3.0])

    assert cosine_similarity(matrix, vector) == pytest.approx(np.array([0.0,1.0,0.0]))

def test_matrix_vector_similarity():
    vector = np.array([1, 0])

    matrix = np.array([[1, 0],
                       [3, 1],
                       [1, 1],
                       [1, 3],
                       [0, 1],
                       [-1, 0],])

    expected = np.array([1.0, 0.948683, 0.707107, 0.316228, 0.0, -1.0])

    assert cosine_similarity(matrix, vector) == pytest.approx(expected)

def test_malformed_matrix_vector():
    vector = np.array([1, 0, 2])

    matrix = np.array([[1, 0],
                       [3, 1],
                       [1, 1],
                       [1, 3],
                       [0, 1],
                       [-1, 0],])

    with pytest.raises(ValueError):
        out = cosine_similarity(matrix,vector)

def test_mixed_input():
    vector = np.array([1, 0, 2])

    matrix = np.array([[1, 0],
                       [3, 1],
                       [1, "2"],
                       [1, "a"],
                       [0, "string"],
                       [-1, 0],])

    with pytest.raises(ValueError):
        out = cosine_similarity(matrix,vector)

def test_empty_input():
    vector = []
    matrix = []

    assert cosine_similarity(matrix, vector) == pytest.approx(0.0)
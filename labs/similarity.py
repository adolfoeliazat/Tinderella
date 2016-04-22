import numpy as np
from scipy.spatial import distance


def euclidean(vec1, vec2):
    '''
    INPUT: 1d array of ints or floats, 1d array of ints or floats
    OUTPUT: float between 0 and 1
    Return the euclidean similarity between vec1 and vec2.
    '''
    return 1.0 / (1 + distance.euclidean(vec1, vec2))


def cosine(vec1, vec2):
    '''
    INPUT: 1d array of ints or floats, 1d array of ints or floats
    OUTPUT: float between 0 and 1
    Return the cosine similarity between vec1 and vec2.
    '''
    norm = np.sqrt(np.dot(vec1, vec1) * np.dot(vec2, vec2))
    if not norm:
        norm = 1
    return 0.5 + 0.5 * np.dot(vec1, vec2) / norm


def pearson(vec1, vec2):
    '''
    INPUT: 1d array of ints or floats, 1d array of ints or floats
    OUTPUT: float between 0 and 1
    Return the pearson similarity between vec1 and vec2.
    '''
    return 0.5 + 0.5 * np.corrcoef(vec1, vec2)[0][1]
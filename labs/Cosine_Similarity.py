import pandas as pd
from sklearn.neighbors import NearestNeighbors


class Recommender(object):
	def __init__(self, feature_matrix, item_path):
		'''
		INPUT:
			- similarity: function, compute similarity metric
			- use_svd: boolean, whether or not to use svd
			- svd_factor: float, if using svd, size of svd matrix (as percent)

		OUTPUT: None
		'''
		self.feature_matrix = feature_matrix
		self.item_path = item_path

def find_nearest_neighbors(self)
	'''
	INPUT: None
	OUTPUT:
		- 5 nearest neighbors of the point
	Return the 5 nearest neighbors.
	'''
	neigh = NearestNeighbors(n_neighbors=5)

	for i in xrange(self.feature_matrix[0]):
		index = neigh.kneighbors(feature_matrix[i], return_distance=False)
		print index

if __name__ == '__main__':
	# test = Recommender(X,item)
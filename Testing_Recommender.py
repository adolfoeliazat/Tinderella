import pandas as pd
from sklearn.neighbors import NearestNeighbors
from collections import defaultdict 
import random
from Pipeline_CommonFunctions import clean_file_lst
import cPickle as pkl


class Recommender(object):
	def __init__(self, feature_matrix, item_path= None):
		'''
		INPUT:
			- feature_matrix: full feature matrix
			- item_path: directory path of image

		OUTPUT: nearest neighbors to each image
		'''
		self.feature_matrix = feature_matrix
		self.item_path = item_path
		self.neighbor_dict = None
		self.full_lst = None

	def get_random_img(self):
		random_img_index = random.sample(range(self.feature_matrix.shape[0]),5)
		for index in random_img_index:
			print index
			print self.item_path[index]
			self.full_lst.append(self.item_path[index])

		return self.full_lst

	def get_likes(self):
		if img == 'like':
			np.append(likes, img)

		return np.mean(np.array([likes]), axis =0)


	def find_nearest_neighbors(self):
		'''
		INPUT: None
		OUTPUT:
			- 5 nearest neighbors of the point
		Return the 5 nearest neighbors.
		'''
		# self.neighbor_dict = defaultdict(list)
		neigh = NearestNeighbors(n_neighbors=20)
		neigh.fit(X)
		with open('/FeatVecs/NN_full50_20neighbors.pkl', 'w') as f:
			pkl.dump(neigh, f)


		neigh2 = NearestNeighbors(n_neighbors=20)
		neigh2.fit(X)

		with open('/FeatVecs/NN_50_20neighbors.pkl', 'w') as f2:
			pkl.dump(neigh2, f2)
		for i in xrange(self.feature_matrix.shape[0]):
			indices = neigh.kneighbors(self.feature_matrix[i], return_distance=False)

			for j, index in enumerate(indices[0]):
				self.neighbor_dict[i].append((index, self.item_path[j]))

		return indices, self.item_path[indices],self.neighbor_dict



if __name__ == '__main__':
	feature_df = pd.read_pickle('/FeatVecs/feature_matrix_test15k.pkl')
	rm = Recommender(X,item_name)
	show_random_img = rm.get_random_img()
	print show_random_img
	avg_img_array = rm.get_likes()
	rm.find_nearest_neighbors(avg_img_array)

	
	


	

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble.partial_dependence import plot_partial_dependence
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np
from scipy.sparse import *
from sklearn.cluster import KMeans

class KMeansClustering(object):
	def __init__(self, feat_matrix, num_clusters, target_arr = None):
		self.feat_matrix = feat_matrix
		self.num_clusters = num_clusters
		self.target_arr = target_arr
		self.train_x = None
		self.train_y = None
		self.test_x = None
		self.test_y = None


	def train_test_split(self):

		self.train_x, self.test_x, self.train_y, self.test_y = train_test_split(self.feat_matrix, self.target_arr, test_size=.2, random_state=1)
		print 'Train x Shape:', self.train_x.shape
		print 'Test x Shape:', self.test_x.shape

	# def pca(self):
	# 	n_col = int(self.train_x.shape[1]*.10)
	# 	pca = PCA(n_components=n_col)
	# 	train_feat = self.train_x
	# 	train_components = pca.fit_transform(train_feat)


	# 	# test_feat = self.test_x
	# 	# test_components = pca.fit_transform(test_feat)
	# 	pca_range = np.arange(min(self.train_x.shape[0],n_col)) + 1
	# 	# xbar_names = ['PCA_%s' % xtick for xtick in pca_range]
	# 	plt.bar(pca_range, pca.explained_variance_ratio_, align='center')
	# 	xticks = plt.xticks(np.arange(0,self.train_x.shape[0], 100), rotation=90)
	# 	plt.ylabel('Variance Explained')
	# 	plt.bar(np.arange(200), pca_ratio[:200], align = 'center')
	# 	xticks = plt.xticks(np.arange(0,200, 10), rotation = 90)
	# 	plt.show()

	# 	return pca.explained_variance_ratio_


	def mksparse(matix):
		Sparse = csc_matrix(matrix)

		return Sparse
	def cross_val(self, estimator, x, y):
		# n_jobs=-1 uses all the cores on your machine
		f1_score = cross_val_score(estimator, x, y,
							   scoring='f1',
							   cv=5, n_jobs=-1) * -1

		params = estimator.get_params()
		name = estimator.__class__.__name__
		print f1_score
		# print '%s Train CV | F1: %.3f' % (name, f1_score)
		
		return f1_score



	def Random_ForestClass(self):
		trans_start = 0
		trans_end = self.train_x.shape[1]
		print self.train_x[:,trans_start:trans_end].shape
		rf = RandomForestClassifier(random_state = 1)
		rf.fit(self.train_x[:,trans_start:trans_end], self.train_y)
		# train_components = pca.fit_transform(train_x)
		# test_components = pca.fit_transform(test_x)
		print self.train_x[:,trans_start:trans_end].shape
		print 'rf score: ', rf.score(self.test_x[:,trans_start:trans_end], self.test_y)
		print 'cross_val: ', self.cross_val(rf,self.test_x[:,trans_start:trans_end],self.test_y )
		print 'avg f1 cross_val: ', sum(self.cross_val(rf,self.test_x[:,trans_start:trans_end],self.test_y )
		)/5.
		# return rf.score(self.test_x[:,trans_start:trans_end], self.test_y)


		

	def Gradient_Boosting(self):

		gdbr = GradientBoostingRegressor(learning_rate=0.1, loss='ls',
										 n_estimators=10000, random_state=1)

		print self.cross_val(gdbr)
		return gdbr.fit(train_x, train_y)


	def grid_search(est, grid):
		grid_cv = GridSearchCV(est, grid, n_jobs=-1, verbose=True,
							  scoring='f1').fit(train_x, train_y)
		return grid_cv

	def kmeans(self):
		kmeans = KMeans(n_clusters = self.num_clusters)
		kmeans.fit(self.feat_matrix)

		return kmeans



	def main(self):
		train_test_split()

		rf = Random_ForestRegress()

		print rf, gbr


		# rf_grid = {'max_depth': [3, None],
		# 		   'max_features': [1, 3, 10],
		# 		   'min_samples_split': [1, 3, 10],
		# 		   'min_samples_leaf': [1, 3, 10],
		# 		   'bootstrap': [True, False],
		# 		   'n_estimators': [30, 1000, 10000],
		# 		   'random_state': [1]}

		# gd_grid = {'learning_rate': [0.1, 0.05, 0.02, 0.01],
		# 		   'max_depth': [4, 6],
		# 		   'min_samples_leaf': [3, 5, 9, 17],
		# 		   'max_features': [1.0, 0.3, 0.1],
		# 		   'n_estimators': [10000],
		# 		   'random_state': [1]}

		# rf_grid_search = self.grid_search(RandomForestRegressor(), rf_grid)
		# gd_grid_search = self.grid_search(GradientBoostingRegressor(), gd_grid)
		# rf_best = rf_grid_search.best_estimator_
		# gd_best = gd_grid_search.best_estimator_



		# # 1. K-Means
		kmeans = KMeans(n_clusters = self.num_clusters)
		kmeans.fit(self.feat_matrix)
		# # 2. Print out the centroids.
		# print "cluster centers:"
		# print kmeans.cluster_centers_





		# # 3. Find the top 10 features for each cluster.
		# top_centroids = kmeans.cluster_centers_.argsort()[:,-1:-11:-1]
		# print "top features for each cluster:"
		# for num, centroid in enumerate(top_centroids):
		#     print "%d: %s" % (num, ", ".join(features[i] for i in centroid))


		# # 4. Limit the number of features and see if the members of the groups change.
		# X[:1000]
		# kmeans = KMeans()
		# kmeans.fit(X)
		# top_centroids = kmeans.cluster_centers_.argsort()[:,-1:-11:-1]
		# print "top features for each cluster with 1000 max features:"
		# for num, centroid in enumerate(top_centroids):
		#     print "%d: %s" % (num, ", ".join(features[i] for i in centroid))


		# # 5. Print out the titles of a random sample of the articles assigned to each
		# # cluster to get a sense of the topic.
		# assigned_cluster = kmeans.transform(X).argmin(axis=1)
		# for i in range(kmeans.n_clusters):
		#     cluster = np.arange(0, X.shape[0])[assigned_cluster==i]
		#     sample_articles = np.random.choice(cluster, 3, replace=False)
		#     print "cluster %d:" % i
		#     for article in sample_articles:
		#         print "    %s" % articles_df.ix[article]['headline']
		

		return k_means.labels_


if __name__ == '__main__':
	# load feature matrix
	# feat_matrix_file = '/Volumes/hermanng_backup/Virginia_Capstone/FeatVecs/rescaled_feat_matrix.csv'
	# feature_matrix = np.loadtxt(feat_matrix_file, delimiter = ',')
	# target_arr_file = '/Volumes/hermanng_backup/Virginia_Capstone/FeatVecs/size_ten_50_50_labels.csv'
	# target_arr = np.loadtxt(target_arr_file, delimiter= ',')
	# KMeansClustering(feature_matrix,9,target_arr)
	# cluster = KMeansClustering(X, 7, y)
	# k = KMeans(n_clusters = 6)
	# k.fit(X)
	# f = open('/Volumes/hermanng_backup/Virginia_Capstone/FeatVecs/kmeansModel.pkl','w')
	# pickle.dump(k, f)

	# neigh = NearestNeighbors(n_neighbors=6)
	# neigh.fit(X)
	# neigh.kneighbors(mean_img_array, return_distance=False)
	# # m = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/nearest_neighbor.pkl','w')
	# # pickle.dump(neigh, m)
	# m.close()
	# cluster.train_test_split()
	# cluster.Random_ForestClass()
	num_clusters = 6
	feat_matrix = X
	target_arr = y

	test15k_100_100 = KMeansClustering(feat_matrix, num_clusters, target_arr)
	test15k_100_100.train_test_split()
	print test15k_100_100.Random_ForestClass()

	import numpy as np
	X = np.load('/Volumes/hermanng_backup/Virginia_Capstone/FeatVecs/rescaled_new_feat_matrix_50_50_10e_test15k.npy')

	with open('/Volumes/hermanng_backup/Virginia_Capstone/FeatVecs/size_new_twenty_50_50_10e_test15k_labels.csv', 'r') as f:
		y = f.read().split(',')

	y_clean = [name for name in y if name]

	num_clusters = 6
	feat_matrix = X
	target_arr = y_clean

	test15k_50_50 = KMeansClustering(feat_matrix, num_clusters, target_arr)
	test15k_50_50.train_test_split()
	print test15k_50_50.Random_ForestClass()










from sklearn.cluster import KMeans
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

class KMeansClustering(object):
	def __init__(self, feat_matrix, target_arr = None, num_clusters):
		self.feat_matrix = feat_matrix
		self.num_clusters = num_clusters
		self.target_arr = target_arr

	def Random_Forest(self):
		train_feat, test_feat, train_target, test_target = train_test_split(self.feat_matrix, self.target_arr, test_size=0.2)
		rf = RandomForestClassifier()
		rf.fit(train_feat, train_target)
		print 'rf score: ', rf.score(test_feat, test_target)
		return rf.score(test_feat, test_target)


	def Gradient_Boosting(self):

		gdbr = GradientBoostingRegressor(learning_rate=0.1, loss='ls',
		                                 n_estimators=100, random_state=1)
		gdbr.fit(train_x, train_y)


	def K_Nearest_Neighbors(self):
		knn = KNeighborsClassifier(n_neighbors=5)
		knn.fit(self.feat_matrix, self.target_arr) 
		print 'knn score: ', knn.score(self.feat_matrix, self.target_arr)
		return knn.score(self.feat_matrix, self.target_arr)

	def main(self):
		# 1. K-Means
		kmeans = KMeans(n_clusters = self.num_clusters)
		kmeans.fit(self.feat_matrix)
		# 2. Print out the centroids.
		print "cluster centers:"
		print kmeans.cluster_centers_
		Random_Forest()
		K_Nearest_Neighbors()





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
	feat_matrix_file = '/Volumes/hermanng_backup/Virginia_Capstone/FeatVecs/rescaled_feat_matrix.csv'
	feature_matrix = np.loadtxt(feat_matrix_file, delimiter = ',')
	target_arr_file = '/Volumes/hermanng_backup/Virginia_Capstone/FeatVecs/size_ten_50_100_labels.csv'
	target_arr = np.loadtxt(target_arr_file, delimiter= ',')
	KMeansClustering(feature_matrix, 9)
	main()












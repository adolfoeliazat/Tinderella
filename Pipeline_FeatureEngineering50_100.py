import scipy
from scipy import ndimage
from skimage import data, io, filter, color
from skimage.transform import resize
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from skimage.filter import roberts, sobel, canny, scharr, rank
import os
import matplotlib.pyplot as plt
import sys
from skimage.feature import CENSURE
from skimage.feature import (match_descriptors, corner_harris,
							 corner_peaks, ORB, plot_matches)
from skimage.util.dtype import dtype_range
from skimage.util import img_as_ubyte
from skimage import exposure
from skimage.filter import threshold_otsu
from skimage.segmentation import felzenszwalb, slic, quickshift
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
import cPickle as pickle


# modules I wrote
from Pipeline_CommonFunctions import clean_file_lst
from test_color_clustering import Color_Clustering

IMAGE_SIZE = (50,50)

def filter_function(img_grey, filt = 'canny'):
	"""
	Grayscales and apply edge detectors to image.
	Returns the flattened filtered image array.
	input: raw image 3d tensor
	output: filtered image
	filters: 'sobel', 'roberts', 'scharr'
	default filter = 'canny'
	"""
	# grayscale filters:
	if filt =='sobel':
		return sobel(img_grey)
	elif filt == 'roberts':
		return roberts(img_grey)
	elif filt == 'canny':
		return canny(img_grey)
	elif filt == 'scharr':
		return scharr(image_grey)
	elif filt == ('canny', 'sobel'):
		return canny(sobel(img_grey))
	else:
		raise Exception('No Such Filter!')

def feature_detectors(img_grey):
	"""
	Extracts features from raw 3d tensor/grayscaled/filtered
	images.

	"""
	# feature detectors:
	censure_detector = CENSURE(mode ='Octagon')
	censure_detector.detect(img_grey)
	censure_keypoints = censure_detector.keypoints
	censure_vec = np.ravel(censure_keypoints)

	orb_descriptor_extractor = ORB(n_keypoints=200)
	orb_descriptor_extractor.detect_and_extract(img_grey)
	orb_keypoints = np.ravel(orb_descriptor_extractor.keypoints)
	orb_descriptors = np.ravel(orb_descriptor_extractor.descriptors)
	orb_vec = np.concatenate((orb_keypoints, orb_descriptors), axis=0)
	feat_det_vec = np.concatenate((censure_vec, orb_vec), axis=0)

	return 	feat_det_vec


def local_eq(img_arr):
	"""
	Spreads out the most frequent intensity values in an image.
	Input: 3D image tensor or 2D grayscaled image or 
		   filtered/transformed image array.
	Ouput: Global equalize with same shape as img_arr
	"""
	return np.ravel(exposure.equalize_hist(img_arr))


def local_threshold(img_arr):
	"""
	For each pixel, an optimal threshold is determined by maximizing 
	the variance between two classes of pixels of the local neighborhood 
	defined by a structuring element.
	
	Input: 	3D image tensor or 2D grayscaled image or 
		   filtered/transformed image array.
	Output: binary img_array where pixels are >= global threshold
	"""

	threshold_global_otsu = threshold_otsu(img_arr)
	global_otsu = img_arr >= threshold_global_otsu

	return np.ravel(global_otsu.astype(int))


class Feature_Engineer(object):

	def __init__(self, stand_img_directory, cached_feature_vector_file, img_size=IMAGE_SIZE, target_size= IMAGE_SIZE
		,filter_funct=filter_function, feat_detect = feature_detectors
		, local_equalize = local_eq, local_thresh = local_threshold):
		"""
		inputs: 
			 main directory containing all lable directories with standardized images
			 shape: tuple: current shape of images
			 target_shape: tuple: target matrix size to run machine learning on.
						   default = current shape
		output: feature_matrix
		"""
		self.stand_img_directory = stand_img_directory
		self.cached_feature_vector_file = cached_feature_vector_file
		self.img_size = img_size
		self.target_size = target_size
		self.filter_funct = filter_funct
		self.feat_detect = feat_detect
		self.local_equalize = local_equalize
		self.local_thresh = local_thresh

	def _check_img_size(self, img_arr, img_file_path):
		# assert size: img.arr.shape = self.shape
		if img_arr.shape[:2] != self.img_size:
			print img_file_path
			print img_arr.shape[:2]
			raise Exception('Image is not the right size!')

	def stand_vector_size(self, arr):
		"""
		Pads/truncates the feature vector into appropriate sizes 
		(usually average feature vector size across all instances)
		"""
		stand_vec_size = 5*self.target_size[0]*self.target_size[0]
		if arr.shape[0] < stand_vec_size:
			return np.append(arr, np.zeros(stand_vec_size - arr.shape[0]))
		else:
			return arr[:stand_vec_size]

		
	def pre_trans(self, img_arr, img_file_path):
		"""
		return pre-filter feature extraction
		For color extraction use color_kmeans()
		local_equalize
		local_threshold
		Segmentation algorithms: felzenszwalb, slic, quickshift
		"""
		# initialize pre_trans vector size
		pre_trans = np.zeros(4*(img_arr.shape[0]*img_arr.shape[1]*img_arr.shape[2]))
		# All extractions using raw colored image array:
		color_kmeans = Color_Clustering(img_file_path, 10, img_arr.shape[:2])
		dom_colors = np.ravel(color_kmeans.main())

		local_eq_raw = self.local_equalize(img_arr)

		local_threshold_raw = self.local_thresh(img_arr)

		# Segmentation: felzenszwalb
		img = img_as_float(img_arr)		                   
		segments_fz = np.ravel(felzenszwalb(img, scale=100, sigma=0.5, min_size=50))
		prior_length = dom_colors.shape[0]+ local_eq_raw.shape[0]+ local_threshold_raw.shape[0] +segments_fz.shape[0]

		# apply feature detection algorithms to grayscaled image
		img_arr_grey = color.rgb2gray(img_arr)
		feat_det_img_arr = self.feat_detect(img_arr_grey)
		stand_feat_det_img_arr = self.stand_vector_size(feat_det_img_arr)
		pre_trans_prior = np.concatenate((dom_colors, local_eq_raw, local_threshold_raw, segments_fz), axis=0)
		pre_trans[:prior_length] = pre_trans_prior
		pre_trans[prior_length:prior_length + stand_feat_det_img_arr.shape[0]] = stand_feat_det_img_arr
		
		return pre_trans, feat_det_img_arr.shape


	def filter_transform(self, img_arr):
		"""
		applying various filters to image array
		Input: transformed image array
		grayscale filters: sobel, roberts, scharr, canny(default)
		feature detectors: CENSURE, ORB
		"""
		# transforms image to gray scale 2D array
		img_arr_grey = color.rgb2gray(img_arr)
		# apply filter to image
		filt_img_arr = self.filter_funct(img_arr_grey)
		
		return filt_img_arr

	def post_trans(self, trans_img_arr):
		# return post-filter feature extraction
		# dominant edges

		'''
		Input: 2d filtered/transformed flattened image array
		Methods: feature_detectors, local histogram equalization, 
		Output: flattened post-transformed image array
		'''
		# # initialize pre_trans vector
		# # apply feature detection to filtered grayscaled image
		feat_det_img_arr = self.feat_detect(trans_img_arr)
		stand_feat_det_img_arr = self.stand_vector_size(feat_det_img_arr)
		# apply local histogram equalization to filtered grayscaled image
		local_eq_trans= self.local_equalize(trans_img_arr)
		local_threshold_trans= self.local_thresh(trans_img_arr)
		# concatenate all feature detectors
		post_trans = np.concatenate((stand_feat_det_img_arr, local_eq_trans, local_threshold_trans),axis=0)

		return np.ravel(post_trans), feat_det_img_arr.shape

	def create_feature_vector(self,pre_features, post_features,unflattened_image) :
		'''
		  Unflattened image is the filtered image
		  First ravel the unflattened filtered image 
		  #column wise concatenate flattened filtered image to label, pre_features
		  and post_features arrays.

		'''
		flat_vect = np.ravel(unflattened_image)
		feat_vec = np.concatenate((pre_features, post_features, flat_vect), axis=0)
		
		return feat_vec

	def rescaling(self, flat_img_arr):
		scaler = StandardScaler()
		rescaled_img_arr = scaler.fit_transform(flat_img_arr)

		return rescaled_img_arr

	def feature_preprocessing(self):
		"""
		main feature preprocessing done
		output: feature_matrix
		"""
		total_feat_det= []
		total_post_feat_detec =[]
		total_post_local =[]
		total_images = 0
		num_failed = 0
		fails =[]
		X = []
		y = []
		full_matrix = []
		label_vec = []
		# f= open('%s/size_ten_50_50_labels.csv'%FeatVecs_path, 'w')
		f = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/size_ten_50_50_10e_labels.csv', 'w')
		clean_stand_img_directory_lst = clean_file_lst(os.listdir(self.stand_img_directory), jpg=False)
		for i, subdir in enumerate(clean_stand_img_directory_lst):
			subdir_path = os.path.join(self.stand_img_directory, subdir)
			clean_img_lst = clean_file_lst(os.listdir(subdir_path), jpg=True)
			for j, img_file in enumerate(clean_img_lst):
				label = subdir
				print label
				# Create path for each image file
				img_file_path = os.path.join(subdir_path, img_file)
				# read in image file
				img_arr = io.imread(img_file_path)
				# Assert image size
				self._check_img_size(img_arr, img_file_path)
				# If self.img_size != self.target_size, reshape to self.target_size
				
				if self.img_size != self.target_size:                        # before or after transformation
					img_arr = resize(img_arr, self.target_size)
				print img_file_path
				# Extract features from raw image array
				try:
					pre_trans_feat,feat_det_size = self.pre_trans(img_arr, img_file_path)
					total_feat_det.append(feat_det_size)
					print 'pre_feat_det', feat_det_size
					print 'pre_trans_feat', pre_trans_feat.shape
				except IndexError:
					num_failed +=1
					fails.append(img_file_path)
					continue

				# Apply filters to transform image array
				unflattened_trans_img_arr = self.filter_transform(img_arr).astype(float)
				print 'trans_img_arr', unflattened_trans_img_arr.shape

				try:
					# Extract features from post-transformed image array
					post_trans_feat, post_feat_det_size= self.post_trans(unflattened_trans_img_arr)
					print 'post_feat_det', post_feat_det_size
					print 'post_trans_feat', post_trans_feat.shape
					total_post_feat_detec.append(post_feat_det_size)

				except IndexError:
					num_failed +=1
					fails.append(img_file_path)
					continue
					#flattened AND concatenated feature vector
				feat_vector= self.create_feature_vector(pre_trans_feat, post_trans_feat,unflattened_trans_img_arr)
				f.write(label + ',')
				label_vec.append(label)
				np.savetxt('%s%s.csv' %(self.cached_feature_vector_file,img_file), feat_vector, fmt='%.10e', delimiter=',') 
			
				print 'feature vector shape', feat_vector.shape
				# Append feature vector and label to full image matrix
				full_matrix.append(feat_vector)
				total_images +=1
				print total_images
					# break

		
		f.close()	
		print 'total_images', total_images
		print 'num_fails', num_failed
		print 'ratio', num_failed/float(total_images)

		# Apply StandardScaler to feature matrix
		rescaled_feat_matrix = self.rescaling(full_matrix)
		np.savetxt('%s/rescaled_feat_matrix_50_50_10e.csv' %FeatVecs_path, rescaled_feat_matrix, fmt='%.10e', delimiter=',') 
		# m = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/feature_matrix.pkl', 'w')
		# pickle.dump(rescaled_feat_matrix, m)

		return rescaled_feat_matrix, label_vec

if __name__ == '__main__':
	dir_path = '/Users/heymanhn/Virginia/Zipfian/Capstone_Project'
	full_dir_path = os.path.join(dir_path, 'Ouput_Images_ten_50_50_percent')
	# FeatVecs_path = os.path.join('/Volumes/hermanng_backup/Virginia_Capstone', 'FeatVecs')
	FeatVecs_path = os.path.join(full_dir_path, 'FeatVecs')
	
	if not os.path.exists(FeatVecs_path):
		print FeatVecs_path
		os.mkdir(FeatVecs_path)

	cach_FeatVecs_path = os.path.join(FeatVecs_path, 'size_ten_50_50_10e_feat/')
	if not os.path.exists(cach_FeatVecs_path):
		os.mkdir(cach_FeatVecs_path)

	fm = Feature_Engineer(full_dir_path, cach_FeatVecs_path, target_size =(50,50))
	X,y= fm.feature_preprocessing()
	# m = open('/Volumes/hermanng_backup/Virginia_Capstone/FeatVecs/feature_matrix.pkl', 'w')
	# pickle.dump(X, m)


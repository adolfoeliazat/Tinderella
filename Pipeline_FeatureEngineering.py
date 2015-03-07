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
from skimage.filters import threshold_otsu

# modules I wrote
from Pipeline_CommonFunctions import clean_file_lst
from test_color_clustering import Color_Clustering
from skimage.filters import threshold_otsu

IMAGE_SIZE = (28,28)

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
	if filt ='sobel':
		return np.ravel(sobel(img_grey))
	elif filt = 'roberts'
		return np.ravel(roberts(img_grey))
	elif filt = 'canny'
		return np.ravel(canny(img_grey))
	elif filt = 'scharr'
		return np.ravel(scharr(image_grey))
	elif filt = ('canny', 'sobel'):
		np.ravel(canny(sobel(img_grey)))
	else
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

	descriptor_extractor = ORB(n_keypoints=200)
	orb_descriptor_extractor.detect_and_extract(img_grey)
	orb_keypoints = orb_descriptor_extractor.keypoints
	descriptors = orb_descriptor_extractor.descriptors
	orb_vec = np.ravel(orb_keypoints)
	feat_det_vec = np.concatenate(censure_vec, orb_vec, axis=0)

	return 	feat_det_vec

def local_eq(img_arr):
	"""
	Spreads out the most frequent intensity values in an image.
	Input: 3D image tensor or 2D grayscaled image or 
	       filtered/transformed image array.
	Ouput: Global equalize with same shape as img_arr
	"""
	return exposure.equalize_hist(img_arr)


def local_threshold(img_arr):
	"""
	For each pixel, an “optimal” threshold is determined by maximizing 
	the variance between two classes of pixels of the local neighborhood 
	defined by a structuring element.
	
	Input: 	3D image tensor or 2D grayscaled image or 
	       filtered/transformed image array.
	Output: binary img_array where pixels are >= global threshold
	"""

	threshold_global_otsu = threshold_otsu(img)
	global_otsu = img >= threshold_global_otsu

	return global_otsu.astype(int)


class Feature_Engineer(object):

	def __init__(self, stand_img_directory, img_size=IMAGE_SIZE, target_size= IMAGE_SIZE
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
		self.img_size = img_size
		self.target_size = target_size
		self.filter_funct = filter_funct
		self.feat_detect = feat_detect
		self.local_equalize = local_equalize
		self.local_thresh = local_thresh

	def _check_img_size(self, img_arr, img_file_path):
		# assert size: img.arr.shape = self.shape
		if img_arr.shape[:2] != self.img_size:
			raise Exception('Image is not the right size!')
			print img_file_path

	def pre_trans(self, img_arr):
		"""
		return pre-filter feature extraction
		For color extraction use color_kmeans()
		Segmentation algorithms: felzenszwalb, slic, quickshift
		"""
		color = color_kmeans(img_arr)
		local_eq_raw = self.local_equalize(img_arr)
		local_threshold_raw = self.local_thresh(img_arr)

		pre_trans = np.concatenate(color, local_eq_raw, local_threshold_raw)
		return np.ravel(pre_trans)


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
		# apply feature detection algorithms to grayscaled image
		feat_det_img_arr = self.feat_detect(img_arr_grey)
		# concatenate all transformations
		trans_img_arr = np.concatenate(filt_img_arr, feat_det_img_arr, axis=0)

		return np.ravel(trans_img_arr)

	def post_trans(self, trans_img_arr):
		# return post-filter feature extraction
		# dominant edges

		'''
	    Input: 2d filtered/transformed flattened image array
	    Methods: feature_detectors, local histogram equalization, 
		Output: flattened post-transformed image array
		'''
		# apply feature detection to filtered grayscaled image
		feat_detect = self.feat_detect(trans_img_arr)
		# apply local histogram equalization to filtered grayscaled image
		local_eq_trans= self.local_equalize(trans_imag_arr)
		local_threshold_trans= self.local_thresh(trans_imag_arr)
		# concatenate all feature detectors
		post_trans = np.concatenate(feat_detect, local_eq_trans, local_threshold_trans,axis=0)

		return np.ravel(post_trans)

	def create_feature_vector(unflattened_image,pre_features,post_features) :
		'''
		  Unflattened image is the filtered image
		  First ravel the unflattened filtered image 
		  #column wise concatenate flattened filtered image to label, pre_features
		  and post_features arrays.

		'''
		flat_vect = np.ravel(unflattened_image)
		feat_vec = np.concatenate(flat_vec, pre_features, post_features, axis = 0)
		
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
		X = []
		y = []
		full_matrix_label = []	
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

				# Extract features from raw image array
				pre_trans_feat = self.pre_trans(img_arr)
				print 'pre_trans_feat', pre_trans_feat.shape
				# Apply filters to transform image array
				trans_img_arr = self.filter_transform(img_arr)
				print 'trans_img_arr', trans_img_arr.shape
				# Extract features from post-transformed image array
				post_trans_feat = self.post_trans(trans_img_arr)
				print 'post_trans_feat', post_trans_feat.shape
				#flattened AND concatenated feature vector
				# print pre_trans_feat
				# print trans_img_arr.shape
				# print post_trans_feat
				feat_vector= self.create_feature_vector(trans_img_arr,pre_trans_feat,post_trans_feat)
				# Append feature vector and label to full image matrix
				full_matrix_label.append((feat_vector, label))


		# # Extract feature matrix from full image matrix
		# # Extract labels from full image_matrix
		# for i in xrange(len(full_matrix_label)):
		# 	X.append(full_matrix_label[i][0])
		# 	y.append(full_matrix_label[i][1])

		# X = np.array(X)
		# y = np.array(y)
		
		# # Apply StandardScaler to feature matrix
		# rescaled_feat_matrix = self.rescaling(X)

		# print rescaled_feat_matrix 


if __name__ == '__main__':
	dir_path = '/Users/heymanhn/Virginia/Zipfian/Capstone_Project'
	full_dir_path = os.path.join(dir_path, 'Test_Output_Images')
	fm = Feature_Engineer(full_dir_path, target_size =(100,100))
	fm.feature_preprocessing()



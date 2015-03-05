import scipy
from scipy import ndimage
from skimage import data, io, filter, color
from skimage.transform import resize
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from skimage.filter import roberts, sobel, canny
import os
import matplotlib.pyplot as plt
import sys
from Pipeline_CommonFunctions.py import clean_file_lst

class Feature_Engineer(object):

	def __init__(self, stand_img_directory, img_size, target_size=None):
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
		target_size = None

	@staticmethod
	def _check_img_size(img_arr, img_file_path):
		# assert size: img.arr.shape = self.shape
		lens = map(len, data_lst)
		if img_arr.size != self.img_size:
			raise Exception('Image is not the right size!')
			print img_file_path

	def pre_trans(self, img_arr):
		# return pre-filter feature extraction
		pass

	def filter_transform(self, img_arr):
		"""
		applying various filters to image array
		input: transformed image array
		"""
		sobel(img_arr)
		roberts(img_arr)

		return trans_img_arr

	def post_trans(self, trans_img_arr):
		# return post-filter feature extraction
		pass

	def flatten(self, img_arr):
		flat_img_arr = img_arr.flatten()[np.newaxis, :]

		return flat_img_arr





	def rescaling(self, flat_img_arr):
		scaler = StandardScaler()
		rescaled_img_arr = scaler.fit_transform(flat_img_arr)

		return rescaled_img_arr


	def feature_preprocessing(self):
		"""
		main feature preprocessing done
		output: feature_matrix
		"""
	
		clean_stand_img_directory_lst = clean_file_lst(os.listdir(self.stand_img_directory), jpg=False)
		for i, subdir in enumerate(clean_stand_img_directory_lst):
			subdir_path = os.path.join(self.stand_img_directory, subdir)
			clean_subdir_lst = self.clean_file_lst(subdir_path, jpg=True)
			full_matrix_label = []
			label = i
			for j, img_file in enumerate(clean_subdir_lst):
				# Create path for each image file
				img_file_path = ps.path.join(subdir_path, img_file)
				# read in image file
				img_arr = io.imread(img_file_path)
				# Assert image size
				self._check_img_size(img_arr, img_file_path)
				# If self.img_size != self.target_size, reshape to self.target_size
				if self.img_size != self.target_size:
					img_arr = reshape(img_arr, self.target_size)

				# Extract features from raw image array
				pre_trans_feat = pre_trans(img_arr)
				# Apply filters to transform image array
				trans_img_arr = filter_transform(pre_img_arr)
				# flatten transformed image array
				rav_trans_img_arr = np.ravel(trans_img_arr)
				# Extract features from post-transformed image array
				post_trans_feat = post_trans(trans_img_arr)
				# Concatenate flattened transformed image array with extracted features
				feat_vector = np.concatenate((rav_trans_img_arr, pre_trans_feat, post_trans_feat), axis=0)
				# Append feature vector and label to full image matrix
				full_matrix_label.append((feat_vector,label))

		# Extract feature matrix from full image matrix
		X = full_matrix_label[:1]
		# Extract labels from full image_matrix
		y = full_matrix_label[0]
		
		# Apply StandardScaler to feature matrix
		rescaled_feat_matrix = self.rescaling(X)

		return feature_matrix


if __name__ == '__main__':
	dir_path = '/Users/heymanhn/Virginia/Zipfian/Capstone_Project/Image_New'
	full_dir_path = os.path.join(dir_path, 'Output_Images')
	fm = Feature_Engineer(full_dir_path, (28, 28))



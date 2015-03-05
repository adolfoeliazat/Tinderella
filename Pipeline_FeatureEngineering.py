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

	def __init__(self, stand_img_directory, shape, target_shape=None):
		"""
		inputs: 
		     main directory containing all lable directories with standardized images
		     shape: tuple: current shape of images
		     target_shape: tuple: target matrix size to run machine learning on.
		                   default = current shape
		output: feature_matrix
		"""
		self.stand_img_directory = stand_img_directory
		self.shape = shape
		target_shape = None

	def flatten(self, img_arr):
		flat_img_arr = img_arr.flatten()[np.newaxis, :]

		return flat_img_arr

	def rescaling(self, flat_img_arr):
		scaler = StandardScaler()
		rescaled_img_arr = scaler.fit_transform(flat_img_arr)

		return rescaled_img_arr


	def sobel_filter(self, img_arr):
		"""
		applying sobel filter to image array
		input: preprocessed image array
		"""

		return sobel(img_arr)	

	def roberts_filter(self, img_arr):
		"""
		applying roberts filter to image array
		input: preprocessed image array
		"""
		pass

	def filter(self, img_array):
		"""
		applying filter to image array
		input: preprocessed image array
		"""	
		pass


	def feature_preprocessing(self):
		"""
		main feature preprocessing done
		output: feature_matrix
		"""
	
		clean_stand_img_directory_lst = clean_file_lst(os.listdir(self.stand_img_directory), jpg=False)
		for subdir in clean_stand_img_directory_lst:
			subdir_path = os.path.join(self.stand_img_directory, subdir)
			clean_subdir_lst = self.clean_file_lst(subdir_path, jpg=True)
			for i, img_file in enumerate(clean_subdir_lst):
				img_mat = np.empty([len(clean_subdir_lst[i]), self.shape[0]*self.shape[1]])
				img_arr = io.imread('shoes/%s' % file_name)
				flat_img_arr = self.flatten(img_arr)
				img_mat[i] = flat_img_arr
				print img_mat.shape
			rescaled_img_mat = self.rescaling(img_mat)
			sobel_mat = self.sobel_filter(rescaled_img_mat)
			filtered_img_mat = sobel_mat
			feature_matrix = filtered_img_mat

		return feature_matrix


if __name__ == '__main__':
	dir_path = '/Users/heymanhn/Virginia/Zipfian/Capstone_Project/Image_New'
	full_dir_path = os.path.join(dir_path, 'Output_Images')
	fm = Feature_Engineer(full_dir_path, (28, 28))



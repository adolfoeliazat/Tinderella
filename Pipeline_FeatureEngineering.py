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

	def __init__(self, stand_img_directory):
		"""
		input: main directory containing all lable directories with standardized images
		output: feature_matrix
		"""
		self.stand_img_directory = stand_img_directory

	def rescaling(self, flat_img_arr):
		scaler = StandardScaler()
		rescaled_img_arr = scaler.fit_transform(flat_img_arr)

		return rescaled_img_arr


	def flatten(self, img_arr):
		flat_img_arr = img_arr.flatten()[np.newaxis, :]

		return flat_img_arr

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
		feature_matrix = []
		clean_stand_img_directory_lst = clean_file_lst(os.listdir(self.stand_img_directory), jpg=False)
		for subdir in clean_stand_img_directory_lst:
			subdir_path = os.path.join(self.stand_img_directory, subdir)
			clean_subdir_lst = self.clean_file_lst(subdir_path, jpg=True)
			for img_file in clean_subdir_lst:
				img_arr = io.imread('shoes/%s' % file_name)
				flat_img_arr = self.flatten(img_arr)
				rescaled_img = self.rescaling(flat_img_arr)
				sobel = self.sobel_filter(rescaled_img)
				feature_matrix.append(sobel)

		return feature_matrix


if __name__ == '__main__':
	dir_path = '/Users/heymanhn/Virginia/Zipfian/Capstone_Project/Image_New'
	full_dir_path = os.path.join(dir_path, 'Output_Images')
	fm = Feature_Engineer(full_dir_path)



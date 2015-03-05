import scipy
from scipy import ndimage
from skimage import data, io, filter, color
from skimage.transform import resize
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
import os

# pwd = u'/Users/heymanhn/Virginia/Zipfian/Capstone_Project/Images'

class Standardize_Images(object):
	"""
	Cleans up and standardizes images, ensuring all images
	are in proper directories.
	Input: Raw images in proper directories.
	Output: Standardized images in output directories
	(same directory structure )
	"""
	def __init__(self, img_size, img_directory='Images_New',
				 path='/Users/heymanhn/Virginia/Zipfian/Capstone_Project/'):
		"""
		input: Size of the generated output image (rows, cols[, dim]). 
		If dim is not provided, the number of channels is preserved.
		"""
		self.img_size = img_size
		self.path = path
		# parent_dirs_path: path to directory consists of all categories
		self.parent_dir_path = os.path.join(path, img_directory) 
		self.uniform_parent_dir_path = None
		self.uniform_parent_dir = 'Output_Images'
		self.output_dir_path = None


	def clean_file_lst(self, file_name_lst, jpg=False):
		"""
		input: list of file/directory file names
		output: cleaned list consisting of only jpg files and non-hidden directories.
		"""
		if not jpg:
			return [fname for fname in file_name_lst if not fname.startswith('.')]
		elif jpg:
			return [fname for fname in file_name_lst if '.jpg' in fname]

	
	def mk_output_directory(self):
		self.uniform_parent_dir_path = os.path.join(self.path, self.uniform_parent_dir)
		clean_parent_dir = self.clean_file_lst(os.listdir(self.parent_dir_path), jpg=False)

		if not os.path.exists(self.uniform_parent_dir_path):
			os.mkdir(self.uniform_parent_dir)
			for subdir in clean_parent_dir:
					self.output_dir_path = os.path.join(self.uniform_parent_dir_path, subdir + '_uniform')
					if not os.path.exists(self.output_dir_path):
						os.mkdir(self.output_dir_path)


	def standardize(self):
		"""
		Iterate over each directory, keeps track of state
		save to output directory
		"""

		clean_parent_dir = self.clean_file_lst(os.listdir(self.parent_dir_path), jpg=False)

		for subdir in clean_parent_dir:
				subdir_path = os.path.join(self.parent_dir_path, subdir)
				clean_subdir = self.clean_file_lst(os.listdir(subdir_path), jpg=True)
				for img_file in clean_subdir:
					self.output_dir_path_pop = os.path.join(self.uniform_parent_dir_path, subdir+ '_uniform')
					img_path = os.path.join(subdir_path, img_file)
					resized_img_arr = self.do_standardize(img_path)
					uniform_img_path = os.path.join(self.output_dir_path_pop, img_file)
					io.imsave(uniform_img_path, resized_img_arr)

					# print self.output_dir_path
					# print img_path
					# io.imsave('%s/%s' % self.output_dir_path, resized_img_arr)

	def do_standardize(self, img_path):
		"""
		Reshape each image
		"""
		print img_path

		img = data.imread(img_path, as_grey=False).astype('int32')
		resized_img_arr = resize(img, self.img_size)
		return resized_img_arr


if __name__ == '__main__':
	s = Standardize_Images((28,28))
	s.mk_output_directory()
	s. standardize()
	


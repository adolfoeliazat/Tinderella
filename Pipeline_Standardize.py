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
        self.category_dirs_path = os.path.join(path, img_directory)
        self.output_dir_path = None

    
    def mk_output_directory(self):
        uniform_parent_dir = os.path.join(self.path,'Output_Images')
        if not os.path.exists(uniform_parent_dir):
            os.mkdir(uniform_parent_dir)
            for category_dir in os.listdir(self.category_dirs_path):
                if not category_dir.startswith("."): ##
                    new_path = os.path.join(uniform_parent_dir, category_dir + '_uniform')
                    if not os.path.exists(new_path):
                        os.mkdir(new_path)
        # self.output_dir_path = uniform_parent_dir

    def clean_file_names(self, file_name_lst, jpg=False):
        if not jpg:
            return [fname for fname in file_name_lst if not fname.startswith('.')]
        elif jpg:
            return [fname for fname in file_name_lst if 'jpg' in fname]

    def standardize(self):
        """
        Iterate over each directory, keeps track of state
        save to output directory
        """

        subdirs = os.listdir(self.category_dirs_path)
        for subdir in subdirs:
            if not subdir.startswith("."): ##
                subdir_path = os.path.join(self.category_dirs_path, subdir)
                for img_file in os.listdir(subdir_path):
                    img_path = os.path.join(subdir_path, img_file)
                    resized_img_arr = self.do_standardize(img_path)
                    io.imsave('Output_Images/%s' % img_file, resized_img_arr)

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
    


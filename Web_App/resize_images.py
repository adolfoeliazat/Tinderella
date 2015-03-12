from skimage import data, io, filter, color
from skimage.transform import resize
import os

img_lst = ['barneys_503325118.jpg', 'barneys_503463453.jpg', 'barneys_503765460.jpg', 
'breaker-red-carpet-best-dressed-oscars-2015-2.jpg',
'nordstrom_1018353.jpg', 'rene-caovilla-pink.jpg', 'rene-orange.jpg', 'rene.gold.jpg', 
'so_kate.jpg', 'so_kate2.jpg']

for img_file in img_lst:
	img_file_path = os.path.join('Web_App/static', img_file)
	img = io.imread(img_file_path)
	resized_img_arr = resize(img,(500,400))
	io.imsave('Web_App/static/resized_%s'%img_file, resized_img_arr)

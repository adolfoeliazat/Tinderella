import scipy
from scipy import ndimage
from skimage import data, io, filter, color
from skimage.transform import resize
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
import os

company = ['saks', 'barneys']
departments = ['athletic', 'boots', 'evening']
# pwd = u'/Users/heymanhn/Virginia/Zipfian/Capstone_Project/Images'
if __name__ == '__main__':
	target_lst = []
    feature_arr = None
	for store in company:
		for i, category in enumerate(departments):
			if os.path.exists('%s/%s' %(store, category)):
    			file_names = os.listdir('%s/%s' %(store, category))

	    		for file_name in file_names:
	 				label = i
					target_lst.append(label)

        			img_arr = scipy.misc.imread('%s/%s/%s' % (store, category,file_name)).astype('int32')


       				dx = ndimage.sobel(img_arr, 0)  # horizontal derivative
        			dy = ndimage.sobel(img_arr, 1)  # vertical derivative
        			mag = np.hypot(dx, dy)  # magnitude
        			mag *= 255.0 / np.max(mag)  # normalize (Q&D)
        			img_arr = mag.flatten()[np.newaxis, :]

        			if feature_arr is None:
            			feature_arr = img_arr
       				else:
            			feature_arr = np.r_[feature_arr, img_arr]

    target_arr = np.array(target_lst)

    train_feat, test_feat, train_target, test_target = train_test_split(feature_arr, target_arr, test_size=0.33)
    rf = RandomForestClassifier()
    rf.fit(train_feat, train_target)
    print rf.score(test_feat, test_target)



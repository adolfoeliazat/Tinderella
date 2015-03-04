
# coding: utf-8

# In[139]:

import scipy
from scipy import ndimage
from skimage.filter.rank import entropy
from skimage.morphology import disk
from skimage import data, io, color
from skimage.transform import resize, downscale_local_mean
from skimage.filter import roberts, sobel,canny
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
import os
import matplotlib.pyplot as plt

get_ipython().magic(u'matplotlib inline')


# In[2]:

company = ['saks', 'barneys']
departments = ['athletic', 'boots', 'evening']

target_lst = []
feature_arr = None

for store in company:
    for i, category in enumerate(departments):
        if os.path.exists('%s/%s' %(store, category)):
            file_names = os.listdir('%s/%s' %(store, category))

            for file_name in file_names:
                label = i
                target_lst.append(label)


# In[13]:

file_name = 'barneys_158585078.jpg'
category = 'boots'
image = data.imread('%s/%s/%s' % (store, category,file_name), as_grey=True).astype('int32')
# img= scipy.misc.imread('%s/%s/%s' % (store, category,file_name)).astype('int32')
print file_name
resized_image = resize(image, (250, 250))


# In[8]:


edge_roberts = roberts(resized_image)
edge_roberts_re = roberts(resized_image)
edge_sobel = sobel(image)


fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(12,7))

ax0.imshow(edge_roberts, cmap=plt.cm.gray)
ax0.set_title('Roberts Edge Detection')
ax0.axis('off')

ax1.imshow(edge_sobel, cmap=plt.cm.gray)
ax1.set_title('Sobel Edge Detection')
ax1.axis('off')


plt.show()


# In[151]:

image = data.imread('%s/%s/%s' % (store, category,file_name), as_grey=False).astype('int32')

fig, ((ax0, ax1), (ax2, ax3), (ax4, ax5)) = plt.subplots(3,2, figsize=(12, 12))

img0 = ax0.imshow(image, cmap=plt.cm.gray)
ax0.set_title('Original Image')
ax0.axis('off')
fig.colorbar(img0, ax=ax0)

# Resized Images
resized_image = resize(image, (250, 250))
image_grey = color.rgb2gray(resized_image)

img1 = ax1.imshow(image_grey, cmap=plt.cm.jet)
ax1.set_title('Grey Original Size')
ax1.axis('off')

img2 = ax2.imshow(image_grey, cmap=plt.cm.jet)
ax2.set_title('Resized Grey')
ax2.axis('off')
# fig.colorbar(img1, ax=ax1)

img3 = ax3.imshow(sobel(image_grey), cmap=plt.cm.jet)
ax3.set_title('Sobel on Grey')
ax3.axis('off')
# fig.colorbar(img1, ax=ax1)

img4 = ax4.imshow(canny(image_grey,sigma=0.0005, low_threshold=1.0*(10^-11), high_threshold=0.9), cmap=plt.cm.jet)
ax4.set_title('canny on Grey')
ax4.axis('off')
# fig.colorbar(img1, ax=ax1)

plt.show()

category = 'boots'


# In[124]:

# CENSURE feature detector
import skimage.transform as tf
from skimage.feature import CENSURE
tform = tf.AffineTransform(scale=(1.5, 1.5), rotation=0.5,
                           translation=(150, -200))

img1 = rgb2gray(resize(image, (250,250)))
img2 = tf.warp(img1, tform)

detector = CENSURE(mode ='Octagon')

fig, ax = plt.subplots(nrows=1, ncols=2)

plt.gray()

detector.detect(image_grey)

ax[0].imshow(image_grey)
ax[0].axis('off')
ax[0].scatter(detector.keypoints[:, 1], detector.keypoints[:, 0],
              2 ** detector.scales, facecolors='none', edgecolors='r')

detector.detect(img2)

ax[1].imshow(img2)
ax[1].axis('off')
ax[1].scatter(detector.keypoints[:, 1], detector.keypoints[:, 0],
              2 ** detector.scales, facecolors='none', edgecolors='r')

plt.show()

detector.detect(image_grey)
detector.keypoints[:, 1]


# In[162]:

canny(resize(rgb2gray(data.lena()), (512, 512)), sigma = 3, )


# In[129]:

ORB Detector
from skimage import data
from skimage import transform as tf
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)
from skimage.color import rgb2gray
import matplotlib.pyplot as plt

original = data.imread('%s/%s/%s' % (store, category,file_name), as_grey=False).astype('int32')
original_resized = rgb2gray(resize(original, (250,250)))
img1 = original_resized
img2 = tf.rotate(img1, 180)
plt.imshow(img1)
tform = tf.AffineTransform(scale=(1.3, 1.1), rotation=0.5,
                           translation=(0, -200))
img3 = tf.warp(img1, tform)

descriptor_extractor = ORB(n_keypoints=20)

descriptor_extractor.detect_and_extract(img1)
keypoints1 = descriptor_extractor.keypoints
descriptors1 = descriptor_extractor.descriptors

# descriptor_extractor.detect_and_extract(img2)
# keypoints2 = descriptor_extractor.keypoints
# descriptors2 = descriptor_extractor.descriptors

# descriptor_extractor.detect_and_extract(img3)
# keypoints3 = descriptor_extractor.keypoints
# descriptors3 = descriptor_extractor.descriptors

# matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)
# matches13 = match_descriptors(descriptors1, descriptors3, cross_check=True)

# fig, ax = plt.subplots(nrows=2, ncols=1)

# plt.gray()

# plot_matches(ax[0], img1, img2, keypoints1, keypoints2, matches12)
# ax[0].axis('off')

# plot_matches(ax[1], img1, img3, keypoints1, keypoints3, matches13)
# ax[1].axis('off')

# plt.show()


# In[138]:

rgb2gray(image)


# In[105]:

# BRIEF binary descriptor
from skimage import data
from skimage import transform as tf
from skimage.feature import (match_descriptors, corner_peaks, corner_harris,
                             plot_matches, BRIEF)
from skimage.color import rgb2gray
import matplotlib.pyplot as plt


img1 = image_grey
tform = tf.AffineTransform(scale=(1.2, 1.2), translation=(0, -100))
img2 = tf.warp(img1, tform)
img3 = tf.rotate(img1, 25)

keypoints1 = corner_peaks(corner_harris(img1), min_distance=3)
keypoints2 = corner_peaks(corner_harris(img2), min_distance=3)
keypoints3 = corner_peaks(corner_harris(img3), min_distance=3)

extractor = BRIEF()

extractor.extract(img1, keypoints1)
keypoints1 = keypoints1[extractor.mask]
descriptors1 = extractor.descriptors

extractor.extract(img2, keypoints2)
keypoints2 = keypoints2[extractor.mask]
descriptors2 = extractor.descriptors

extractor.extract(img3, keypoints3)
keypoints3 = keypoints3[extractor.mask]
descriptors3 = extractor.descriptors

matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)
matches13 = match_descriptors(descriptors1, descriptors3, cross_check=True)

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(12,12))

plt.gray()

plot_matches(ax[0], img1, img2, keypoints1, keypoints2, matches12)
ax[0].axis('off')

plot_matches(ax[1], img1, img3, keypoints1, keypoints3, matches13)
ax[1].axis('off')

plt.show()


# In[170]:

from skimage.feature import daisy
from skimage import data
import matplotlib.pyplot as plt
img = image_grey
descs, descs_img = daisy(img, step=180, radius=100, rings=2, histograms=6,
                         orientations=8, visualize=True)

fig, ax = plt.subplots()
ax.axis('off')
ax.imshow(descs_img)
descs_num = descs.shape[0] * descs.shape[1]
ax.set_title('%i DAISY descriptors extracted:' % descs_num)
plt.show()


# In[ ]:




# In[ ]:

import scipy
from scipy import ndimage
from skimage.filter.rank import entropy
from skimage.morphology import disk
from skimage import data, io, color
from skimage.transform import resize, downscale_local_mean
from skimage.filter import roberts, sobel,canny
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
import os
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

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
                    if '.jpg' in file_name:
                        label = i
                        target_lst.append(label)
#                         print store, category, file_name
                        image = data.imread('%s/%s/%s' %(store, category, file_name), as_grey=False).astype('int32')
                        resized_image = resize(image, (250, 250))
                        image_grey = color.rgb2gray(resized_image)

                        mag = image_grey

    #                     dx = ndimage.sobel(img_grey, 0)  # horizontal derivative
    #                     dy = ndimage.sobel(img_grey, 1)  # vertical derivative
    #                     mag = np.hypot(dx, dy)  # magnitude
    #                     mag *= 255.0 / np.max(mag)  # normalize (Q&D)
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


# In[ ]:




# In[54]:

image_grey


# In[26]:

mag.shape


# In[28]:

img_arr.shape


# In[32]:

scipy.misc.imread('%s/%s/%s' % (store, category,file_name)).astype('int32').shape


# In[ ]:




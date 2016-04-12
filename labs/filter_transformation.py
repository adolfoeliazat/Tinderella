
# coding: utf-8

# In[57]:

import scipy
from scipy import ndimage
from skimage.filter.rank import entropy
from skimage.morphology import disk
from skimage import data, io, color
from skimage.transform import resize, downscale_local_mean
from skimage.filter import roberts, sobel,canny, scharr
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
import os
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

path ='/Users/heymanhn/Virginia/Zipfian/Capstone_Project/Test_Output_Images/boots'
file_name ='barneys_158585078.jpg'
image = io.imread('%s/%s' %(path,file_name))
plt.imshow(image)
image_grey = color.rgb2gray(image)


# In[58]:

edge_roberts = roberts(image_grey)
edge_canny = canny(image_grey)
edge_sobel = sobel(image_grey)
edge_scharr = scharr(image_grey)


# In[59]:

fig, ((ax0, ax1), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12,7))

ax0.imshow(edge_roberts, cmap=plt.cm.gray)
ax0.set_title('Roberts Edge Detection')
ax0.axis('off')

ax1.imshow(edge_canny, cmap=plt.cm.gray)
ax1.set_title('Canny Edge Detection')
ax1.axis('off')

ax3.imshow(edge_sobel, cmap=plt.cm.gray)
ax3.set_title('Sobel Edge Detection')
ax3.axis('off')

ax4.imshow(edge_scharr, cmap=plt.cm.gray)
ax4.set_title('Scharr Edge Detection')
ax4.axis('off')


plt.show()


# In[13]:

fig, ((ax0, ax1), (ax2, ax3), (ax4, ax5)) = plt.subplots(3,2, figsize=(12, 12))

img0 = ax0.imshow(image, cmap=plt.cm.gray)
ax0.set_title('Original Image')
ax0.axis('off')
fig.colorbar(img0, ax=ax0)

# Resized Images
resized_image = resize(image, (28, 28))
image_grey = color.rgb2gray(resized_image)

img1 = ax1.imshow(image_grey, cmap=plt.cm.jet)
ax1.set_title('Grey Original Size')
ax1.axis('off')

img2 = ax2.imshow(image_grey, cmap=plt.cm.jet)
ax2.set_title('Resized Grey')
ax2.axis('off')
fig.colorbar(img1, ax=ax1)

img3 = ax3.imshow(sobel(image_grey), cmap=plt.cm.jet)
ax3.set_title('Sobel on Grey')
ax3.axis('off')
fig.colorbar(img1, ax=ax1)

img4 = ax4.imshow(canny(image_grey,sigma=0.0005, low_threshold=1.0*(10^-11), high_threshold=0.9), cmap=plt.cm.jet)
ax4.set_title('canny on Grey')
ax4.axis('off')
# fig.colorbar(img1, ax=ax1)

plt.show()

category = 'boots'
edge_sobel.shape


# In[15]:

# CENSURE feature detector
import skimage.transform as tf
from skimage.feature import CENSURE
tform = tf.AffineTransform(scale=(1.5, 1.5), rotation=0.5,
                           translation=(0, -100))

# tf.AffineTransform(scale=(1.2, 1.2), translation=(0, -100))
img1 = color.rgb2gray(resize(image, (250,250)))
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
print detector.keypoints


# In[16]:

# ORB Detector
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)

im1 = color.rgb2gray(resize(image, (100,100)))
img2 = tf.rotate(img1, 180)
tform = tf.AffineTransform(scale=(1.5, 1.5), rotation=0.5,
                           translation=(0, -100))
img3 = tf.warp(img1, tform)

descriptor_extractor = ORB(n_keypoints=200)

descriptor_extractor = ORB(n_keypoints=20)

descriptor_extractor.detect_and_extract(img1)
keypoints1 = descriptor_extractor.keypoints
descriptors1 = descriptor_extractor.descriptors

descriptor_extractor.detect_and_extract(img2)
keypoints2 = descriptor_extractor.keypoints
descriptors2 = descriptor_extractor.descriptors

descriptor_extractor.detect_and_extract(img3)
keypoints3 = descriptor_extractor.keypoints
descriptors3 = descriptor_extractor.descriptors

matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)
matches13 = match_descriptors(descriptors1, descriptors3, cross_check=True)

fig, ax = fig, ax = plt.subplots(nrows=2, ncols=1, figsize = (12,7))

plot_matches(ax[0], img1, img2, keypoints1, keypoints2, matches12)
ax[0].axis('off')

plot_matches(ax[1], img1, img3, keypoints1, keypoints3, matches13)
ax[1].axis('off')

plt.show()

print keypoints1


# In[49]:

# BRIEF binary descriptor
from skimage.feature import (match_descriptors, corner_peaks, corner_harris,
                             plot_matches, BRIEF)

im1 = color.rgb2gray(resize(image, (267, 231)))
tform = tf.AffineTransform(scale=(1.2, 1.2), translation=(0, -100))
img2 = tf.warp(img1, tform)
img3 = tf.rotate(img1, 25)

keypoints1 = corner_peaks(corner_harris(img1), min_distance=10)
print keypoints1
keypoints2 = corner_peaks(corner_harris(img2), min_distance=3)
keypoints3 = corner_peaks(corner_harris(img3), min_distance=3)

extractor = BRIEF()

extractor.extract(img1, keypoints1)
keypoints1 = keypoints1[extractor.mask]
print keypoints1
descriptors1 = extractor.descriptors
print descriptors1

extractor.extract(img2, keypoints2)
keypoints2 = keypoints2[extractor.mask]
descriptors2 = extractor.descriptors

extractor.extract(img3, keypoints3)
keypoints3 = keypoints3[extractor.mask]
descriptors3 = extractor.descriptors

# matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)
# matches13 = match_descriptors(descriptors1, descriptors3, cross_check=True)

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(12,12))

plt.gray()


# plot_matches(ax[0], img1, img2, keypoints1, keypoints2, matches12)
# ax[0].axis('off')

# plot_matches(ax[1], img1, img3, keypoints1, keypoints3, matches13)
# ax[1].axis('off')

plt.show()


# In[51]:

from skimage.feature import (match_descriptors, corner_peaks, corner_harris,
                             plot_matches, BRIEF)

im1 = color.rgb2gray(resize(image, (267, 231)))
tform = tf.AffineTransform(scale=(1.2, 1.2), translation=(0, -100))
img2 = tf.warp(img1, tform)
img3 = tf.rotate(img1, 25)

keypoints1 = corner_peaks(corner_harris(img1), min_distance=3)
print keypoints1
keypoints2 = corner_peaks(corner_harris(img2), min_distance=3)
keypoints3 = corner_peaks(corner_harris(img3), min_distance=3)

extractor = BRIEF()

extractor.extract(img1, keypoints1)
keypoints1 = keypoints1[extractor.mask]
print keypoints1
descriptors1 = extractor.descriptors
print descriptors1


# In[35]:

image.shape


# In[ ]:




# In[ ]:




# In[ ]:




# In[50]:

# 3 segmentation algorithms: felzenszwalb, slic, quickshift
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np

from skimage.segmentation import felzenszwalb, slic, quickshift
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float

img = img_as_float(resize(image, (100, 100)))
# img = img_as_float(resize(image, (50, 50)))
                   
segments_fz = felzenszwalb(img, scale=100, sigma=0.5, min_size=50)
segments_slic = slic(img, n_segments=250, compactness=10, sigma=1)
segments_quick = quickshift(img, kernel_size=3, max_dist=6, ratio=0.5)

print("Felzenszwalb's number of segments: %d" % len(np.unique(segments_fz)))
print("Slic number of segments: %d" % len(np.unique(segments_slic)))
print("Quickshift number of segments: %d" % len(np.unique(segments_quick)))

fig, ax = plt.subplots(1, 3)
fig.set_size_inches(8, 3, forward=True)
fig.subplots_adjust(0.05, 0.05, 0.95, 0.95, 0.05, 0.05)

ax[0].imshow(mark_boundaries(img, segments_fz))
ax[0].set_title("Felzenszwalbs's method")
ax[1].imshow(mark_boundaries(img, segments_slic))
ax[1].set_title("SLIC")
ax[2].imshow(mark_boundaries(img, segments_quick))
ax[2].set_title("Quickshift")
for a in ax:
    a.set_xticks(())
    a.set_yticks(())
plt.show()


# In[41]:

segments_slic.shape


# In[63]:

np.ravel(edge_sobel).shape


# In[ ]:




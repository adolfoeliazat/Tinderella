import struct
from PIL import Image
import scipy
import scipy.misc
import scipy.cluster

NUM_CLUSTERS = 5

print 'reading image'
filename = '/Users/heymanhn/Virginia/Zipfian/Capstone_Project/Images_Old/barneys/evening/barneys_502192370.jpg'
img = Image.open(filename).resize( (60,60) )
img = img.resize( (28,28), Image.ANTIALIAS)     # optional, to reduce time
ar = scipy.misc.fromimage(img)
shape = ar.shape
ar = ar.reshape((scipy.product(shape[:2]), shape[2]))
print ar.shape

print 'finding clusters'
codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
print 'cluster centres:\n', codes

# vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
# counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

# index_max = scipy.argmax(counts)                    # find most frequent
# peak = codes[index_max]
# colour = ''.join(chr(c) for c in peak).encode('hex')
# print 'most frequent is %s (#%s)' % (peak, colour)
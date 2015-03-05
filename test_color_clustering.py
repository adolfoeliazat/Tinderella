import struct
import Image
import scipy
import scipy.misc
import scipy.cluster
import os



class Color_Clustering(object):
	def __init__(self, img_file_path, num_clusters, img_size):
		self.main_path = '/Users/heymanhn/Virginia/Zipfian/Capstone_Project/Images_Old/barneys'
		self.img_file_path = img_file_path
		self.num_clusters = num_clusters
		self.img_size = img_size

	def main(self):
		print 'reading image'
		filename = os.path.join(self.main_path,self.img_file_path)
		img = Image.open(filename)
		img = img.resize(self.img_size, Image.ANTIALIAS) 
		arr = scipy.misc.fromimage(img)
		ar = arr.reshape((scipy.product(arr.shape[:2]), arr.shape[2]))
		print 'img_reshaped to size:'ar.shape
		print 'finding clusters'
		codes, dist = scipy.cluster.vq.kmeans(ar, self.num_clusters)
		print 'cluster centres:\n', codes

		vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
		counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

		index_max = scipy.argsort(counts) [::-1]           # find most frequent in desc order
		for i in codes[index_max]:
			colour = ''.join(chr(c) for c in i).encode('hex')
			print 'most frequent is %s (#%s)' % (i, colour)


		# # bonus: save image using only the N most common colours
		# c = ar.copy()
		# for i, code in enumerate(codes):
		#     c[scipy.r_[scipy.where(vecs==i)],:] = code
		# scipy.misc.imsave('clusters.png', c.reshape(*shape))
		# print 'saved clustered image'

if __name__ == '__main__':
	img_file_path = 'evening/barneys_502192370.jpg'
	color = Color_Clustering(img_file_path, 5, (28,28))
	color.main()

# im.getcolors()
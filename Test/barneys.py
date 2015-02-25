import numpy as np
import json
import string
import requests
from PIL import Image
from StringIO import StringIO



with open('barneys2.json') as f:
	barneys_json = json.load(f)

item_nums = {}
for i in xrange(len(barneys_json[u'data'])):
	item = barneys_json[u'data'][i]
	item_name = item['name'][0].encode('ascii','ignore')
	item_num_uni = barneys_json[u'data'][i][u'item_num'][0].split()[2]
	item_num_str = item_num_uni.encode('ascii','ignore')
	item_image_url = 'http://product-images.barneys.com/is/image/Barneys/'+\
					 item_num_str + '_product_1?$product_size$'
	item_nums[item_name] = item_image_url 

# 'http://product-images.barneys.com/is/image/Barneys/502699235_product_1?$product_size$


test_url = 'http://product-images.barneys.com/is/image/Barneys/503177039_product_1?$product_size$'
response = requests.get(test_url)
i = Image.open(StringIO(response.content))
image_mat = np.asarray(i)
# RGB2 = im2uint8(RGB1)
[m,n,d]=image_mat.shape
if response.status_code == 200:
    f = open('test.jpg', 'wb')
    f.write(response.content)
    f.close


from bs4 import BeautifulSoup
import requests
import re
from pymongo import MongoClient
from bson.objectid import ObjectId
import argparse
import os
from mongodb import MongoDB
from itertools import izip

# Command line arguments

parser = argparse.ArgumentParser(description='Input Category and Number of Pages')
parser.add_argument("category", help="Category of shoes", type=str)
parser.add_argument('num_pages',type=int,
                   help='Number of Pages in Category')
args = parser.parse_args()

class SaksScraper(object):

	def __init__(self, category, num_pages):

		"""
		:param category: The category you are searching for, e.g. flats /heels
		:return: None
		Define the category, base url and a variable to store the links to all pages.
		"""
		self.category = category.lower()
		self.company = 'saks'
		self.base_url = {'http://www.saksfifthavenue.com/Shoes/Sandals/shop/_/N-52k0st/Ne-6lvnb5?FOLDER%3C%3Efolder_id='}
		
		self.all_pages = []
		
		self.params = {'Folder_id": self.folder_id, 'Nao': 0}
		self.num_pages = int(num_pages)
		self.mongo = MongoDB(db_name = 'shoes', table_name = category)


	def join_url(self):
		"""
		Concatenate the base_url and category and page number
		"""
		folder_id_dict = {'boots': '2534374306624250', 'evening': '2534374306624256',
						'exotic': '2534374306624257','flats': '2534374306624248',
					 'mules&slides':'2534374306626182', 'wedges':'2534374306624276',
					 'pumps&slingbacks':'2534374306624262', 'sandals':'2534374306624269',
					 'sneakers':'2534374306624274', 'wedding':'2534374306624275',
					 'oxfords&loafers&moccasins':'2534374306624258'}
		folder_id = folder_id_dict[self.category]
		return self.base_url + folder_id + '&Nao='

	def get_page_links(self):
		for i in xrange(self.num_pages):
			self.all_pages.append(self.join_url() + str(i*60))


	@staticmethod
	def _check_data_len(data_lst):
		lens = map(len, data_lst):
		if len(set(lens)) > 1:
			raise Exception('Number of Descriptions and Images Do Not Match!')

	def _get_img(self, image_tags, category, ipage, orientation='front'):
		img_lst = []
		for i, tag in enumerate(img_tags):
			item_id = (ipage + 1) * i
			img_link = tag['src']
			img = request.get(img_link).content
			product_id = re.search(r"(?P<product_id>\d+)\_(\d+)",image_link).group("product_id")
			img_lst.append(img)
			if not os.path.exits(category):
				os.makedir(category)
			f = open('%s/%s_%s_%s.jpg' % (category, self.company,product_id, item_id), 'w')
            f.write(img)
            f.close()



    @staticmethod
    def _get_text(txt_tags):
            return [tag.text.strip() for tag in txt_tags]

    def _get_page_content(self, link, ipage):
    	"""
    	:param html: The HTML page as string
    	:return: None
    	Get all info
    	"""
    	html = requests.get(link).content
    	soup = BeautifulSoup(html, 'html.parser')


    	 # Use CSS selectors to get the tags containing the info we want
        designer_name_tags = soup.select('span.product-designer-name')
        description_tags = soup.select('p.product-description')
        price_tags = soup.select('span.product-price')
        front_img_tags = soup.select('img.pa-product-large')
        # Check if the list of tags are all of the same length
        self._check_data_len([designer_name_tags, description_tags, price_tags])

        # Scrape all the info from the page
        designer_name = self._get_text(designer_name_tags)
        description = self._get_text(description_tags)
        price = self._get_text(price_tags)
        self._get_img(front_img_tags, self.category, ipage, orientation='front')

        return izip(description, designer_name, price)


    def _insert_into_db(self,json):
    	self.mongo.insertion(json)

   	def main(self):
   	"""
   	Runs the scraping looping through the pages
   	"""
   	self.get_page_links()
   	print 'Number of Pages = ' ,len(self.all_pages)
   	for i, link in enumerate(self.all_pages):
   		data_tuples = self._get_page_content(link, i)
   		fields = ['description', 'designer_name', 'price']
   		for i, tup in enumerate(data_tuples):
   			if len(fields) != len(tup):
   				raise Exception('Fields Must Have The Same Length As Values') 	
   			json = dict(zip(fields, tup))
   			json ['product_id'] = '%s_%s_%s' %(self.company,self.category, i)
   			self.__insert_into_db(json)

if __name__ == '__main__':
	sk = SaksScraper(args.category, args.num_pages)
	sk.main()


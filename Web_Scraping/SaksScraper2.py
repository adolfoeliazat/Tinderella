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
args = parser.parse_args()

class SaksScraper(object):

	def __init__(self, category):

		"""
		:param category: The category you are searching for, e.g. flats /heels
		:return: None
		Define the category, base url and a variable to store the links to all pages.
		"""
		self.category = category.lower()
		self.company = 'saks'
		self.base_url = 'http://www.saksfifthavenue.com/Shoes/'
		
		self.all_links = []
		
		self.params = {'Nao': 0}
		self.mongo = MongoDB(db_name = 'shoes', table_name = self.category)


	def join_url(self):

		"""
		Concatenate the base_url and category and page number
		"""
		category_dict = {'boots':'Boots/shop/_/N-52k0sa/Ne-6lvnb5?FOLDER<>folder_id=2534374306624250',
					 		'evening':'Evening/shop/_/N-52k0sg/Ne-6lvnb5?FOLDER<>folder_id=2534374306624256',
							'exotics':'Exotics/shop/_/N-52k0sh/Ne-6lvnb5?FOLDER<>folder_id=2534374306624257',
							'flats':'Flats/shop/_/N-52k0s8/Ne-6lvnb5?FOLDER<>folder_id=2534374306624248',
					 		'mules_slides':'Mules-and-Slides/shop/_/N-52k29y/Ne-6lvnb5?FOLDER<>folder_id=2534374306626182',
					  		'wedges':'Wedges/shop/_/N-52k0t0/Ne-6lvnb5?FOLDER<>folder_id=2534374306624276',
					 		'pumps_slingbacks':'Pumps-and-Slingbacks/shop/_/N-52k0sm/Ne-6lvnb5?FOLDER<>folder_id=2534374306624262',
					  		'sandals':'Sandals/shop/_/N-52k0st/Ne-6lvnb5?FOLDER<>folder_id=2534374306624269',
					 		'sneakers':'Sneakers/shop/_/N-52k0sy/Ne-6lvnb5?FOLDER<>folder_id=2534374306624274', 
					 		'wedding':'Wedding/shop/_/N-52k0sz/Ne-6lvnb5?FOLDER<>folder_id=2534374306624275',
					 		'oxfords_loafers_moccasins':'Oxfords-Loafers-and-Moccasins/shop/_/N-52k0si/Ne-6lvnb5?FOLDER<>folder_id=2534374306624258'}

		param_str = ''
		category_url = category_dict[self.category]
		for key, val in self.params.iteritems():
			param_str += '&%s=%s' % (key, val)

		return str(self.base_url + category_url + param_str)


	def get_page_links(self):

		"""
		Base on the first page, get all the links to all the pages
		and assign to instance variable
		"""
		initial_link = self.join_url()
		soup = BeautifulSoup(requests.get(initial_link).content, 'html.parser')
		# Get the number of total pages
		total_pages = int(soup.select('span.totalNumberOfPages')[0].text)
		# Produce the links to each of the pages (each page has 180 results)
		for ipage in range(total_pages):
		    self.params['Nao'] = ipage * 60
		    page_link = self.join_url()
		    self.all_links.append(page_link)


	@staticmethod
	def _check_data_len(data_lst):
		lens = map(len, data_lst)
		if len(set(lens)) > 1:
			raise Exception('Number of Descriptions and Images Do Not Match!')


	def _get_img(self, img_tags, category, orientation='front'):
		img_lst = []
		for i, tag in enumerate(img_tags):
			img_link = tag['src']
			img = requests.get(img_link).content
			product_id = re.search(r"(?P<product_id>\d+)\_(\d+)",img_link).group("product_id")
			img_lst.append(img)
			path = 'Images/%s/%s' % (self.company, category)
			if not os.path.exists(path):
				os.makedirs(path)
			f = open('Images/%s/%s/%s_%s.jpg' % (self.company, category, self.company, product_id), 'w')
			f.write(img)
			f.close()



	@staticmethod
	def _get_text(txt_tags):
		return [tag.text.strip() for tag in txt_tags]


	def _get_page_content(self, link):

		"""
		:param html: The HTML page as string
		:return: None
		Get all info
		"""
		html = requests.get(link).content
		soup = BeautifulSoup(html, 'html.parser')
		product_id = []
		product_link = []

		# Use CSS selectors to get the tags containing the info we want
		designer_name_tags = soup.select('span.product-designer-name')
		description_tags = soup.select('p.product-description')
		price_tags = soup.select('span.product-price')
		front_img_tags = soup.select('img.pa-product-large')
		product_link_tags = soup.select('a.mainBlackText')

		# css selector for product id and product link
		for img_item in front_img_tags:
			product_id.append(re.search(r"(?P<product_id>\d+)\_(\d+)",img_item['src']).group("product_id"))

		for link_item in product_link_tags:
			product_link.append(link_item['href'])

		# Check if the list of tags are all of the same length
		self._check_data_len([product_id, designer_name_tags, description_tags, price_tags, product_link])

		# Scrape all the info from the page
		designer_name = self._get_text(designer_name_tags)
		description = self._get_text(description_tags)
		price = self._get_text(price_tags)
		self._get_img(front_img_tags, self.category, orientation='front')
		category = [self.category for i in xrange(len(product_id))]
		company = [self.company for i in xrange(len(product_id))]
		return izip(category, company, product_id, designer_name, description, price, product_link)

	def _print_result(self, json):
		print json

	def _insert_into_db(self,json):
		self.mongo.insertion(json)

	def main(self):

		"""
		Runs the scraping looping through the pages
		"""
		self.get_page_links()
		print 'category = ' , self.category
		print 'Number of Pages = ' ,len(self.all_links)
		count = 0		
		for i, link in enumerate(self.all_links):
			# For each page, each product gets assigned a tuple containing 
			# prpduct_id,description, designer_name, price
			data_tuples = self._get_page_content(link)
			fields = ['category','company','product_id', 'designer_name', 'description', 'price', 'product_link']
			for i, tup in enumerate(data_tuples):
				count += 1
				if len(fields) != len(tup):
					raise Exception('Fields Must Have The Same Length As Values') 	
				json = dict(zip(fields, tup))
				# self._print_result(json)
				self._insert_into_db(json)
		print 'total_items: ', count
		print 'Done!'

if __name__ == '__main__':
	sk = SaksScraper(args.category)
	sk.main()


from bs4 import BeautifulSoup
import requests
import re
# import MongoDB modules
from pymongo import MongoClient
from bson.objectid import ObjectId


class SaksScraper(object):
	def __init__(self, category, num_pages):
		"""
		:param category: The category you are searching for, e.g. flats /heels
		:return: None
		Define the category, base url and a variable to store the links to all pages.
		"""

		self.base_url = {''http://www.saksfifthavenue.com/Shoes/Sandals/shop/_/N-52k0st/Ne-6lvnb5?FOLDER%3C%3Efolder_id=2534374306624269&Nao=''}
		self.company = 'saks'
		self.all_pages = []
		self.category = category
		self.num_pages = num_pages
		self.mongo = MongoDB(db_name = self.company, table_name = category)


		def page_url(self):
			"""
			Concatenate the base_url and category and page number
			"""
			self.all_pages = [base_url + str(i*60) for i in range(num_pages)]
	def saks(self):
		
		# page_urls = [self.base_url + str(i*60) for i in range(0,self.num_pages)]

		counter = 0
		product_dict_name = {}
		product_dict_url  = {}

		for u in xrange(1,self.num_pages+1):
		# # Category = 'sneakers'
		    params = { 'page' : u }
		    response = requests.get(base_url, params=params)
			soup = BeautifulSoup(response.content, 'html.parser')
			img_lst = soup.select('div.image-container-large .pa-product-large')
			product_lst = soup.select('div.image-container-large a[href]')


			for image_item in img_lst:
			    try:
			        image_link = image_item['src']
			        title = image_item['title']

			        if image_link.startswith('http'):
			            product_id = re.search(r"(?P<product_id>\d+)\_(\d+)",image_link).group("product_id")
			            product_dict_name [product_id] = re.split(" - ", title)

			            image = requests.get(image_link).content

			            counter += 1

			            print counter, ',', product_id
			            f = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/saks/images/%s_%s.png' % str(self.category, product_id)
			                     , 'w')
			            b = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/saks/text/ProductNames_%s.txt' % self.category,'w')
			    
			            f.write(image)
			            b.write(str(product_dict_name))
			    except:
			        pass

			for product_item in product_lst:
			    try: 
			        
			        product_id2 = re.search(r"(\w+)\-(?P<product_id>\d+)",product_item['id']).group("product_id")
			        product_link = product_item['href']

			        if product_link.startswith('http'):
			            product_dict_url [product_id2] = product_link

			            w = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/saks/text/ProductURL_%s.txt' % self.category, 'w') 
			            w.write(str(product_dict_url))
			    except:
			        pass


	def nordstrom(self):


		for u in xrange(1,self.num_pages+1):
		# # Category = 'sneakers'
		    params = { 'page' : u }
		    response = requests.get(base_url, params=params)

		    soup = BeautifulSoup(response.content, 'html.parser')
		    img_lst = soup.select('div.fashion-photo')
		    product_lst = soup.select('div.info.default.women.adult')

		    for image_item in img_lst:
		        try:
		            image_link = image_item.img['data-original']
		            title = image_item.img['alt']

		            if image_link.startswith('http'):
		                product_id = re.search(r"\_(?P<product_id>\d+)\.", image_link).group("product_id")
		                product_dict_name[product_id] = title

		                image = requests.get(image_link).content

		                counter += 1

		                print counter, ',', title
		                f = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/nordstrom/images/sneakers_%s.png' % str(product_id)
		                         , 'w')
		                b = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/nordstrom/text/ProductNames_sneakers.txt','w')
		        
		                f.write(image)
		                b.write(str(product_dict_name))
		        except:
		            pass

		    for product_item in product_lst:
		        try: 
		            product_id = re.search(r"\/(?P<product_id>\d+)\?", product_item.a['href']).group("product_id")
		            product_link = product_item.a['href']
		            product_dict_url [product_id] = product_link

		            w = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/nordstrom/text/ProductURL_sneakers.txt', 'w')
		            w.write(str(product_dict_url))
		        except:
		            pass

	def mongo_import(self):
		mongoimport --db nyt_dump --collection articles  articles_mongoimport.json

		db = client.Vcapstone
		collection = db.heels

		if not collection.find_one(r.json()['parse']):
    		collection.insert(r.json()['parse'])



if __name__ == '__main__':
	main()






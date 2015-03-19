from bs4 import BeautifulSoup
import requests
import re
from pymongo import MongoClient
from bson.objectid import ObjectId
import argparse
import os
from mongodb import MongoDB
from itertools import izip
import math

# Command line arguments

parser = argparse.ArgumentParser(
    description='Input Category and Number of Pages')
parser.add_argument("category", help="Category of shoes", type=str)
args = parser.parse_args()


class BarneysScraper(object):

    def __init__(self, category):
        """
        :param category: The category you are searching for, e.g. flats /heels
        :return: None
        Define the category, base url and a variable to store the
        links to all pages.
        """
        self.category = category.lower()
        self.company = 'barneys'
        self.base_url = 'http://www.barneys.com/barneys-new-york/women/shoes/'

        self.all_links = []

        self.params = {'start': 0}
        self.mongo = MongoDB(db_name='shoes', table_name=self.category)

    def join_url(self):
        """
        Concatenate the base_url and category and page number
        """
        category_dict = {'boots': 'boots',
                         'evening': 'evening',
                         'flats': 'flats',
                         'wedges': 'wedges',
                         'pumps_slingbacks': 'heels',
                         'sandals': 'sandals',
                         'sneakers': 'sneakers'}
        param_str = ''
        category_url = category_dict[self.category]
        for key, val in self.params.iteritems():
            param_str += '&%s=%s' % (key, val)

        return str(self.base_url + category_url + '#sz=48' + param_str)

    def get_page_links(self):
        """
        Base on the first page, get all the links to all the pages
        and assign to instance variable
        """
        initial_link = self.join_url()
        soup = BeautifulSoup(requests.get(initial_link).content, 'html.parser')
        # Get the number of total products, then get the number of total pages
        total_products = soup.select('div.results-hits')[0].text
        total_num_products = re.search(
            r"(?P<num_products>\d+) Products",
            total_products).group("num_products")
        total_pages = int(math.ceil(float(total_num_products) / 48))
        # Produce the links to each of the pages (each page has 180 results)
        for ipage in range(total_pages):
            self.params['start'] = ipage * 48
            page_link = self.join_url()
            self.all_links.append((page_link, {'start': ipage * 48}))

    @staticmethod
    def _check_data_len(data_lst):
        lens = map(len, data_lst)
        if len(set(lens)) > 1:
            raise Exception('Number of Descriptions and Images Do Not Match!')

    def _get_img(self, img_tags, category, orientation='front'):
        img_lst = []
        for i, tag in enumerate(img_tags):
            img_link = tag['data-image-alter']
            img = requests.get(img_link).content
            product_id = re.search(
                r"\/(?P<product_id>\d+)\_(\w+)",
                img_link).group("product_id")
            img_lst.append(img)
            path = 'Images/%s/%s' % (self.company, category)
            if not os.path.exists(path):
                os.makedirs(path)
            f = open(
                'Images/%s/%s/%s_%s.jpg' %
                (self.company,
                 category,
                 self.company,
                 product_id),
                'w')
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
        print link[0]
        print link[1]
        html = requests.get(link[0], params=link[1]).content
        soup = BeautifulSoup(html, 'html.parser')
        product_id = []
        product_link = []

        # Use CSS selectors to get the tags containing the info we want
        designer_name_tags = soup.select('a.brand-link')
        description_tags = soup.select('a.name-link')
        price_tags = soup.select('span.product-sales-price')
        front_img_tags = soup.select('.gridImg')
        product_link_tags = soup.select('a.mainBlackText')

        # css selector for product id and product link
        for item in description_tags:
            product_id.append(
                re.search(
                    r"\-(?P<product_id>\d+)\.",
                    item['href']).group("product_id"))
            product_link.append(item['href'])

        # Check if the list of tags are all of the same length
        self._check_data_len([product_id, designer_name_tags, description_tags,
                              price_tags, product_link])

        # Scrape all the info from the page
        designer_name = self._get_text(designer_name_tags)
        description = self._get_text(description_tags)
        price = self._get_text(price_tags)
        self._get_img(front_img_tags, self.category, orientation='front')
        category = [self.category for i in xrange(len(product_id))]
        company = [self.company for i in xrange(len(product_id))]
        return izip(
            category,
            company,
            product_id,
            designer_name,
            description,
            price,
            product_link)

    def _print_result(self, json):
        print json

    def _insert_into_db(self, json):
        self.mongo.insertion(json)

    def main(self):
        """
        Runs the scraping looping through the pages
        """
        self.get_page_links()
        print 'category = ', self.category
        print 'Number of Pages = ', len(self.all_links)
        count = 0
        for i, link in enumerate(self.all_links):
            # For each page, each product gets assigned a tuple containing
            # prpduct_id,description, designer_name, price
            data_tuples = self._get_page_content(link)
            fields = [
                'category',
                'company',
                'product_id',
                'designer_name',
                'description',
                'price',
                'product_link']
            for i, tup in enumerate(data_tuples):
                count += 1
                if len(fields) != len(tup):
                    raise Exception(
                        'Fields Must Have The Same Length As Values')
                json = dict(zip(fields, tup))
                self._insert_into_db(json)
                # self._print_result(json)
        print 'total_items: ', count
        print 'Done!'

if __name__ == '__main__':
    br = BarneysScraper(args.category)
    br.main()

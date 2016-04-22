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


class NordstromScraper(object):

    def __init__(self, category):
        """
        :param category: The category you are searching for, e.g. flats /heels
        :return: None
        Define the category, base url and a variable to
        store the links to all pages.
        """
        self.category = category.lower()
        self.company = 'nordstrom'
        self.base_url = 'http://shop.nordstrom.com/c/'

        self.all_links = []

        self.params = {'page': 1}
        self.mongo = MongoDB(db_name='shoes', table_name=self.category)

    def join_url(self):
        """
        Concatenate the base_url and category and page number
        """
        category_dict = {'athletic': 'womens-athletic-shoes-shop',
                         'booties': 'booties',
                         'boots': 'womens-boots',
                         'espadrilles': 'espadrilles-for-women',
                                        'evening': 'womens-evening-shoes',
                                        'flats': 'womens-flats',
                                        'mules_clogs': 'womens-mules-clogs',
                                        'wedges': 'wedges-for-women',
                                        'pumps': 'womens-pumps',
                                        'sandals': 'womens-sandals-shop',
                                        'sneakers': 'womens-sneakers'}
        param_str = ''
        category_url = category_dict[self.category]
        for key, val in self.params.iteritems():
            param_str += '&%s=%s' % (key, val)

        return str(self.base_url + category_url + '?origin=leftnav')

    def get_page_links(self):
        """
        Base on the first page, get all the links to all the pages
        and assign to instance variable
        """
        initial_link = self.join_url()
        soup = BeautifulSoup(requests.get(initial_link).content, 'html.parser')
        # Get the number of total products, then get the number of total pages
        total_num_products = int(soup.select('span.count')[0].text)
        print total_num_products
        total_pages = int(math.ceil(float(total_num_products) / 100))
        # Produce the links to each of the pages (each page has 180 results)
        for ipage in range(1, total_pages + 1):
            self.params['page'] = ipage
            page_link = self.join_url()
            self.all_links.append((page_link, {'page': ipage}))

    @staticmethod
    def _check_data_len(data_lst):
        lens = map(len, data_lst)
        if len(set(lens)) > 1:
            raise Exception('Number of Descriptions and Images Do Not Match!')

    def _get_img(self, img_tags, product_tags, category, orientation='front'):
        img_lst = []
        product_id = []

        for i, id_tag in enumerate(product_tags):
            product_id.append(id_tag['data-style-number'])

        for i, tag in enumerate(img_tags):
            img_link = tag.img['data-original']
            img = requests.get(img_link).content
            img_lst.append(img)

            self._check_data_len([product_id[:i + 1], img_lst])
            path = 'Images/%s/%s' % (self.company, category)
            if not os.path.exists(path):
                os.makedirs(path)
            f = open(
                'Images/%s/%s/%s_%s.jpg' %
                (self.company,
                 category,
                 self.company,
                 product_id[i]),
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

        r = open('/Users/heymanhn/Desktop/r.html', 'w')
        r.write(str(soup))
        r.close()
        designer_name_tags = []
        description_tags = []
        product_id = []
        product_link = []

        # Use CSS selectors to get the tags containing the info we want
        title_tags = soup.select('a.title')
        price_tags = [
            i.text for i in soup.findAll(
                "span", {
                    "class": 'price'})
            if 'Was' not in i.text and 'OFF' not in i.text]
        front_img_tags = soup.select('div.fashion-photo')
        product_id_tags = soup.select('div.fashion-item')
        product_link_tags = soup.select('a.fashion-href')

        # css selector for product id and product link
        for tit_tag in title_tags:
            designer_name_tags.append(re.split("'", tit_tag.text)[0])
            description_tags.append("".join(re.split("'", tit_tag.text)[1:]))
            product_link.append('http://shop.nordstrom.com' + tit_tag['href'])

        for id_tag in product_id_tags:
            product_id.append(id_tag['data-style-number'])

        for link_tag in product_link_tags:
            product_link.append(link_tag['href'])

        # Check if the list of tags are all of the same length
        self._check_data_len([product_id,
                              designer_name_tags,
                              description_tags,
                              price_tags,
                              product_link])

        # Scrape all the info from the page
        designer_name = designer_name_tags
        description = description_tags
        price = price_tags
        self._get_img(
            front_img_tags,
            product_id_tags,
            self.category,
            orientation='front')
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
    br = NordstromScraper(args.category)
    br.main()

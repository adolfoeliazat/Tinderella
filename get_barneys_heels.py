from bs4 import BeautifulSoup
import requests
import re

url1 = 'http://shop.nordstrom.com/c/womens-athletic-shoes-shop?origin=leftnav#category=b6012093&type=category&defaultsize3=&size=&width=&color=&price=&brand=&stores=&instoreavailability=false&lastfilter=&sizeFinderId=8&resultsmode=&segmentId=0&page='

url2 = '&partial=1&pagesize=100&contextualsortcategoryid=0&shopperSegment=1-0-2%7C3M2%3ARS'

page_url = [url1+ str(i) + url2  for i in range(1,4)]



counter = 0
product_dict_name = {}
product_dict_url  = {}

for u in xrange(len(page_url)):
# # Category = 'heels'
    response = requests.get(page_url[u])
    soup = BeautifulSoup(response.content, 'html.parser')
    img_lst = soup.select('div.product-tile .gridImg')
    product_lst = soup.select('div.product-tile .brand-link')

    for image_item in img_lst:
        try:
            image_link = image_item['src']
            title = image_item['title']

            if image_link.startswith('http'):
                product_id = re.search(r"\/(?P<product_id>\d+)\_(\d+)", image_link).group("product_id")
                product_dict_name [product_id] = title

                image = requests.get(image_link).content

                counter += 1

                print counter, ',', product_id
                f = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/nordstroms/images/athletic_%s.png' % str(product_id)
                         , 'w')
                b = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/nordstroms/text/ProductNames_athletic.txt','w')
        
                f.write(image)
                b.write(str(product_dict_name))
        except:
            pass

    for product_item in product_lst:
        try: 
            product_id = re.search(r"\-(?P<product_id>\d+)\.",product_item['href']).group("product_id")
            product_link = product_item['href']

            if product_link.startswith('http'):
                product_dict_url [product_id] = product_link

                w = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/barneys/text/ProductURL_athletic.txt', 'w')
                w.write(str(product_dict_url))
        except:
            pass




# test = 'http://www.barneys.com/tabitha-simmons-jenny-wedge-espadrilles-503694705.html'
# re.search(r"\-(?P<product_id>\d+)\.", test).group("product_id")

# ''
# test = 'http://product-images.barneys.com/is/image/Barneys/503741202_1_shoeside?$grid_flexH$'
# re.search(r"\/(?P<product_id>\d+)\_(\d+)", test).group("product_id")

from bs4 import BeautifulSoup
import requests
import re


base_url = 'http://www.barneys.com/barneys-new-york/women/shoes/boots#sz=48'
num_pages = 8



counter = 0
product_dict_name = {}
product_dict_url  = {}
product_dict_brand = {}

for u in xrange(num_pages):
# # Category = 'boots'
    params = { 'start' : str(int(u*48))}
    response = requests.get(base_url, params=params)
    # r = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/barneys/text/test.html', 'w')
    # r.write(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')
    img_lst = soup.select('.gridImg')
    product_lst = soup.select('.brand-link')

    for image_item in img_lst:
        try:
            image_link = image_item['data-image-alter']
            title = image_item['title']

            if image_link.startswith('http'):
                product_id = re.search(r"\/(?P<product_id>\d+)\_(\w+)", image_link).group("product_id")
                product_dict_name [product_id] = title

                image = requests.get(image_link).content

                counter += 1

                print counter, ',', product_id
                f = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/barneys/images/boots_%s.png' % str(product_id)
                         , 'w')
                b = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/barneys/text/ProductNames_boots.txt','w')
        
                f.write(image)
                b.write(str(product_dict_name))
        except:
            pass

    for product_item in product_lst:
        try: 
            product_id = re.search(r"\-(?P<product_id>\d+)\.",product_item['href']).group("product_id")
            product_link = product_item['href']
            product_brand = re.split('\n\t\t\t', str(product_item))[-1]

            if product_link.startswith('http'):
                product_dict_url[product_id] = product_link
                product_dict_brand[product_id] = product_brand

                w = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/barneys/text/ProductURL_boots.txt', 'w')
                w.write(str(product_dict_url))
                w.write(str(product_dict_brand))
        except:
            pass




# test = 'http://www.barneys.com/tabitha-simmons-jenny-wedge-espadrilles-503694705.html'
# re.search(r"\-(?P<product_id>\d+)\.", test).group("product_id")

# ''
# test = 'http://product-images.barneys.com/is/image/Barneys/503741202_1_shoeside?$grid_flexH$'
# re.search(r"\/(?P<product_id>\d+)\_(\d+)", test).group("product_id")

# test = http://product-images.barneys.com/is/image/Barneys/502734973_product_1?$grid_flexH$




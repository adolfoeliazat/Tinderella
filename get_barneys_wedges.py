from bs4 import BeautifulSoup
import requests
import re


base_url = 'http://www.barneys.com/barneys-new-york/women/shoes/wedges#start='
page_url = [base_url + str(i*48) +'&sz=48'  for i in range(0,2)]



counter = 0
product_dict_name = {}
product_dict_url  = {}

for u in xrange(len(page_url)):
# # Category = 'wedges'
    response = requests.get(page_url[u])
    soup = BeautifulSoup(response.content, 'html.parser')
    img_lst = soup.select('div.product-tile .product-image.grid_flexH .gridImg')
    product_lst = soup.select('div.product-tile .brand-link')

    for image_item in img_lst:
        try:
            image_link = image_item['src']
            title = image_item['title']

            if image_link.startswith('http'):
                product_id = re.search(r"\/(?P<product_id>\d+)\_(\d+)", image_link).group("product_id")
                product_dict_name [product_id] = re.split(" - ", title)

                image = requests.get(image_link).content

                counter += 1

                print counter, ',', product_id
                f = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/barneys/images/wedges_%s.png' % str(product_id)
                         , 'w')
                b = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/barneys/text/ProductNames_wedges.txt','w')
        
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

                w = open('/Users/heymanhn/Virginia/Zipfian/Capstone_Project/barneys/text/ProductURL_wedges.txt', 'w')
                w.write(str(product_dict_url))
        except:
            pass




# test = 'http://www.barneys.com/tabitha-simmons-jenny-wedge-espadrilles-503694705.html'
# re.search(r"\-(?P<product_id>\d+)\.", test).group("product_id")

# ''
# test = 'http://product-images.barneys.com/is/image/Barneys/503741202_1_shoeside?$grid_flexH$'
# re.search(r"\/(?P<product_id>\d+)\_(\d+)", test).group("product_id")

src="http://product-images.barneys.com/is/image/Barneys/503475106_shoe3?$grid_flexH$" data-original="http://product-images.barneys.com/is/image/Barneys/503475106_shoe3?$grid_flexH$" data-image-alter="http://product-images.barneys.com/is/image/Barneys/503475106_shoe1?$grid_flexH$" onerror="this.src='http://demandware.edgesuite.net/aasv_prd/on/demandware.static/Sites-BNY-Site/-/default/v1425190603657/images/browse_placeholder_image.jpg'" 
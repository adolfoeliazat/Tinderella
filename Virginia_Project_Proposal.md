# Project name: Tinderella ('A dream is a wish your heart makes')

# Summary: 


	> Do you have time to scroll through more than 5000 pairs of shoes on Neiman Marcus?

	> Tinderella acts like a personal shoe stylist that learns each user's unique and exquisite taste in
	> shoes and gives recommendations.



# Motivation: Why are you doing this project?

	> In 2014, Women shoes alone account for over $20 Billion in revenue. A good pair of shoes make our
	> outfits stand out. It allows us to show off our personalities. It elongates our figures. The
	> biggest problem we face when shopping for shoes is that many shoe brands label their shoes by
	> name, making it very difficult to remember. Style descriptions are not 100% accurate and effective
	> either. Morever, current marketing campaign do not take into personal preferences. 


# Deliverables: How will you demonstrate your project? Will you have a web app? Blog posts? Everyone will be doing a presentation, but you also need to be able to demo your project to someone who doesn't see your presentation.


	> Web app with user interactions: 

	> Users first give their preferences by rating 'hot' or 'not'(may also be multi-criteria). 
	> The recommender system then generates a list of recommended shoes based on the items shown to them
	> The app returns a set of photos with prices and links to retailer.


# Data Sources: Where are you getting your data (include links!)


	> 1) [Zappos Women's Shoes](http://www.zappos.com/womens-shoes~1i7)

	> 2) [Nordstrom Women's Shoes](http://shop.nordstrom.com/c/womens-shoes?origin=leftnav)

	> 3) [Barneys Women's Shoes](http://www.barneys.com/on/demandware.store/Sites-BNY-Site/default/Search
	> -Show?cgid=womens-shoes)

	> 4) [Saks Women's Shoes](http://www.saksfifthavenue.com/Shoes/shop/_/N-52k0s7/Ne-6
	> lvnb5?FOLDER%3C%3Efolder_id=2534374306624247)

	> 5) [Neiman Marcus Women's Shoes](http://www.neimanmarcus.com/Shoes/cat000141/c.
	> cat?siloId=cat000141&navid=topNavShoes)

	> 6) [heels.com](http://www.heels.com/)


# Process: What will your approach be? This of course will adapt as you get deeper into the project, but you should have a high level idea of the tasks you need to do. What web scraping, feature engineering, model building, app building, etc do you need to do?


	> 1) Scrape image, text(brand, style name, price, brief description) from data sources.

	> 2) Image Data Storage: take  each image link, converts it into uint8 (m, m, 3) matrix and stores 
	> it into a file.

	> 3) Image preprocessing: apply filters (ex: Sobel Edge Detection Filter), downsample image matrix, 
	> apply pyramid match kernal.

	> 4) Build recommender (Unsupervised- Clustering, Supervised - Multinomial): based mainly on 
	> similarity between images. Also takes into account text data: color, material etc. Possibly multi-
	> criteria. 

	** Tools Used: OpenCV, SciKit.Image, Unsupervised/Supervised Learning. 













